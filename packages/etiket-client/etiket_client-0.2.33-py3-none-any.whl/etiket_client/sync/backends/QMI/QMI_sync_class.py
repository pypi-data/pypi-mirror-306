from etiket_client.remote.endpoints.models.types import FileType
from etiket_client.sync.base.sync_source_abstract import SyncSourceDatabaseBase, SyncSourceFileBase
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item

from datetime import datetime, timedelta
import os, pathlib, dataclasses, xarray, re, xarray

class QuantifySync(SyncSourceFileBase):
    SyncAgentName = "QMI"
    ConfigDataClass = QuantifyConfigData
    MapToASingleScope = True
    LiveSyncImplemented = False
    level = 2
    
    @staticmethod
    def rootPath(configData: QuantifyConfigData) -> pathlib.Path:
        return pathlib.Path(configData.quantify_directory)

    @staticmethod
    def checkLiveDataset(configData: QuantifyConfigData, syncIdentifier: sync_item, maxPriority: bool) -> bool:
        if not maxPriority:
            return False
        
        # check the last time the file is modified:
        dir_content = os.listdir(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier))
        m_files = [content for content in dir_content if content.endswith(".hdf5") or content.endswith(".h5")]
        
        if len(m_files) == 0:
            return False

        m_file = max(m_files, key=lambda f: os.path.getmtime(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, f)))
        path = os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, m_file)
        mod_time = pathlib.Path(path).stat().st_mtime
        if datetime.now() - datetime.fromtimestamp(mod_time) < timedelta(minutes=2):
            return True
        return False
    
    @staticmethod
    def syncDatasetNormal(configData: QuantifyConfigData, syncIdentifier: sync_item):
        create_ds_from_quantify(configData, syncIdentifier, False)
        path = pathlib.Path(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier))
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.startswith("."): # ignore hidden files (e.g. .DS_Store)
                    continue
                
                relative_path = os.path.relpath(os.path.join(root, file), start=path)
                name_parts = [re.sub(r"\d{8}-\d{6}-\d{3}-[a-z0-9]{6}-", "", part)
                                for part in pathlib.Path(relative_path).parts]
                name = ".".join(name_parts)
        
                file_name = file
                file_path = os.path.join(root, file)
                
                if file.endswith(".hdf5") or file.endswith(".h5"):
                    f_info = file_info(name = name, fileName = file_name,
                                        created = datetime.fromtimestamp(pathlib.Path(os.path.join(root, file)).stat().st_mtime),
                                        fileType = FileType.HDF5_NETCDF, file_generator = "QMI")
                    ds = xarray.load_dataset(file_path, engine='h5netcdf')
                    
                    # check if fields in the datasets are standard deviations and mark them as such -- this is useful for plotting
                    data_vars = list(ds)
                    for var_name in data_vars:
                        if var_name.endswith("_u") and var_name[:-2] in data_vars:
                            ds[var_name[:-2]].attrs['__std'] = var_name
                            ds[var_name].attrs['__is_std'] = 1
                    
                    sync_utilities.upload_xarray(ds, syncIdentifier, f_info)
                else:
                    f_info = file_info(name = name, fileName = file_name,
                        created = datetime.fromtimestamp(pathlib.Path(os.path.join(root, file)).stat().st_mtime),
                        fileType = FileType.UNKNOWN, file_generator = "QMI")
                    
                    sync_utilities.upload_file(file_path, syncIdentifier, f_info)
    
    @staticmethod
    def syncDatasetLive(configData: QuantifyConfigData, syncIdentifier: sync_item):
        create_ds_from_quantify(configData, syncIdentifier, True)
        raise NotImplementedError


def create_ds_from_quantify(configData: QuantifyConfigData, syncIdentifier: sync_item, live : bool):
    tuid = syncIdentifier.dataIdentifier.split('/')[1][:26]
    name = syncIdentifier.dataIdentifier.split('/')[1][27:]
    created = datetime.strptime(tuid[:18], "%Y%m%d-%H%M%S-%f")
    
    # get variable names in the dataset, this is handy for searching!
    keywords = set()
    try:
        xr_ds = xarray.load_dataset(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, "dataset.hdf5"), engine='h5netcdf')
        
        for key in xr_ds.keys():
            if 'long_name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['long_name'])
                continue
            if 'name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['name'])

        for key in xr_ds.coords:
            if 'long_name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['long_name'])
                continue
            if 'name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['name'])  
    except:
        pass
    
    ds_info = dataset_info(name = name, datasetUUID = syncIdentifier.datasetUUID,
                alt_uid = tuid, scopeUUID = syncIdentifier.scopeUUID,
                created = created, keywords = list(keywords), 
                attributes = {"set-up" : configData.set_up})
    sync_utilities.create_ds(live, syncIdentifier, ds_info)
    