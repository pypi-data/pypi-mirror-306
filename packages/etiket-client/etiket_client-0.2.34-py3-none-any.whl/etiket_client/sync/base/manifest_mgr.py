from dataclasses import dataclass, field
from typing import Dict, Optional
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os, logging, typing

if typing.TYPE_CHECKING:
    from watchdog.observers.api import BaseObserverSubclassCallable

logger = logging.getLogger(__name__)


class manifest_manager:
    __manifest_contents = {}
    
    def __init__(self, name : str, root_path : Path = None, current_manifest : Dict[str, float] = None,  level : int = 1):
        '''
        initialise the manifest manager with the name of the dataset and the root path of the dataset.
        
        Args:
            name (str) : the name of the dataset
            root_path (Path) : the root path of the dataset
            current_manifest (Dict[str, float]) : the current manifest that contains the keys of the datasets and the last modified time of the dataset.
            level (int) : the depth of folders at which the datasets are stored. Default is 1.
        '''
        self.name = name
        if name in self.__manifest_contents:
            self.state = self.__manifest_contents[name]
        else:
            logger.debug("Initializing manifest manager for %s", name)
            self.state = manifest_state(root_path, current_manifest, level)
            logger.debug("Initialized manifest manager for %s", name)
            self.__manifest_contents[name] = self.state
    
    def get_last_change(self, data_identifier : str) -> float:
        '''
        Get the current manifest of the dataset. This can be used to compare changes.
        '''
        return self.state.get_last_change(data_identifier)
    
    def push_update(self, identifier : str, priority : float):
        '''
        Push manually an update to the manifest manager.
        '''
        self.state.update_queue[identifier] = priority
        
    def get_updates(self) -> Dict[str, int]:
        '''
        Get changes in the manifest since last update call.
        '''
        updates = {**self.state.update_queue}
        self.state.update_queue.clear()
        return updates

@dataclass
class manifest_state:
    root_path: Path
    current_manifest: dict
    level : int
    update_queue: Dict[str, float] = field(default_factory=dict)
    file_watcher: Optional['BaseObserverSubclassCallable'] = None
    
    def __post_init__(self):
        self.file_watcher = get_observer(self.root_path, self.level, self.update_queue)
        new_manifest = manifest_get(self.root_path, self.level)
        diff_manifest = manifest_diff(self.current_manifest, new_manifest)
        diff_manifest.update(self.update_queue)
        self.update_queue.update(diff_manifest)

    def get_last_change(self, identifier : str) -> float:
        manifest_path = Path.joinpath(self.root_path, *identifier.split('/'))
        return manifest_get(manifest_path, 0)['']

def get_observer(root_path : Path, level : int, update_queue : Dict[str, float]) -> 'BaseObserverSubclassCallable':
    observer = Observer()
    observer.schedule(file_watcher(root_path, level, update_queue), root_path, recursive=True)
    observer.start()
    return observer

class file_watcher(FileSystemEventHandler):
    def __init__(self, root_path : Path, level : int, update_queue : Dict[str, float]):
        super().__init__()
        self.root_path = root_path
        self.level = level
        self.update_queue = update_queue
    
    def on_created(self, event):
        if event.src_path.endswith('.DS_Store'):
            return
        self.add_update(Path(event.src_path))
    
    def on_modified(self, event):
        if event.src_path.endswith('.DS_Store'):
            return
        self.add_update(Path(event.src_path))
        
    def on_moved(self, event):
        if event.src_path.endswith('.DS_Store'):
            return
        self.add_update(Path(event.dest_path))
        
    def add_update(self, path : Path):
        path = path if os.path.isdir(path) else Path(os.path.dirname(path))
        path_parts = path.relative_to(self.root_path).parts[:self.level]
        if len(path_parts) >= self.level:
            key_name = "/".join(path_parts[:self.level])
            self.update_queue[key_name] = os.stat(path).st_mtime

def manifest_get(base_directory : Path, level : int) -> Dict[str, float]:
    manifest  = {}
    base_depth = len(base_directory.parts)

    for root, _, files in os.walk(base_directory):
        current_depth = len(Path(root).parts) - base_depth
        if current_depth >= level:
            for file in files:
                mod_time = os.stat(f"{root}/{file}").st_mtime
                key_name = "/".join(Path(root).relative_to(base_directory).parts[:level])
                manifest[key_name] = max(manifest.get(key_name, 0), mod_time)

    return manifest

def manifest_diff(old_manigest : Dict[str, float], new_manifest : Dict[str, float]) -> Dict[str, float]:
    differences = {}
    for key in new_manifest.keys():
        if key in old_manigest and old_manigest[key] == new_manifest[key]:
            continue
        differences[key] = new_manifest[key]
    return differences