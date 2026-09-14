"""
File change detection module
Handles real-time file system change monitoring
"""

import logging
import os
import time
from typing import Optional, Dict, Any, List, Set, Callable
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler, FileSystemEvent

class ChangeMonitor:
    """Monitor file system changes in real-time"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.observer = Observer()
        self.handlers = {}
        self.started = False
        
    def start_monitoring(self) -> None:
        """Start the file system monitor"""
        if not self.started:
            self.observer.start()
            self.started = True
            
    def stop_monitoring(self) -> None:
        """Stop the file system monitor"""
        if self.started:
            self.observer.stop()
            self.observer.join()
            self.started = False
            
    def watch_directory(self,
                       path: str,
                       recursive: bool = True,
                       patterns: Optional[List[str]] = None,
                       ignore_patterns: Optional[List[str]] = None,
                       callback: Optional[Callable[[FileSystemEvent], None]] = None
                       ) -> None:
        """Watch a directory for changes"""
        try:
            path_obj = Path(path)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {path}")
                
            # Create event handler
            handler = FileChangeHandler(
                patterns=patterns,
                ignore_patterns=ignore_patterns,
                callback=callback,
                logger=self.logger
            )
            
            # Schedule directory watching
            self.observer.schedule(
                handler,
                str(path_obj),
                recursive=recursive
            )
            
            # Store handler reference
            self.handlers[str(path_obj)] = handler
            
            if not self.started:
                self.start_monitoring()
                
        except Exception as e:
            self.logger.error(f"Error watching directory: {str(e)}")
            
    def unwatch_directory(self, path: str) -> None:
        """Stop watching a directory"""
        try:
            path_obj = Path(path)
            
            # Remove handler
            if str(path_obj) in self.handlers:
                handler = self.handlers[str(path_obj)]
                self.observer.unschedule(handler)
                del self.handlers[str(path_obj)]
                
        except Exception as e:
            self.logger.error(f"Error unwatching directory: {str(e)}")
            
    def get_recent_changes(self, path: str, minutes: int = 60) -> List[Dict[str, Any]]:
        """Get recent changes in a directory"""
        try:
            path_obj = Path(path)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {path}")
                
            changes = []
            cutoff_time = time.time() - (minutes * 60)
            
            # Walk directory
            for root, dirs, files in os.walk(str(path_obj)):
                for name in files + dirs:
                    try:
                        file_path = Path(root) / name
                        stat_result = file_path.stat()
                        
                        # Check if modified within time window
                        if stat_result.st_mtime >= cutoff_time:
                            changes.append({
                                "path": str(file_path),
                                "type": "directory" if file_path.is_dir() else "file",
                                "modified": datetime.fromtimestamp(stat_result.st_mtime),
                                "size": stat_result.st_size if file_path.is_file() else None
                            })
                    except Exception as e:
                        self.logger.error(f"Error processing {file_path}: {str(e)}")
                        continue
                        
            return sorted(changes, key=lambda x: x["modified"], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error getting recent changes: {str(e)}")
            return []
            
class FileChangeHandler(FileSystemEventHandler):
    """Handle file system change events"""
    
    def __init__(self,
                 patterns: Optional[List[str]] = None,
                 ignore_patterns: Optional[List[str]] = None,
                 callback: Optional[Callable[[FileSystemEvent], None]] = None,
                 logger: Optional[logging.Logger] = None):
        super().__init__()
        self.patterns = patterns
        self.ignore_patterns = ignore_patterns
        self.callback = callback
        self.logger = logger or logging.getLogger(__name__)
        
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file/directory creation"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Created: {event.src_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling creation event: {str(e)}")
            
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file/directory modification"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Modified: {event.src_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling modification event: {str(e)}")
            
    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file/directory deletion"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Deleted: {event.src_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling deletion event: {str(e)}")
            
    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file/directory move/rename"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Moved/Renamed: {event.src_path} -> {event.dest_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling move event: {str(e)}")
            
    def _should_handle_event(self, event: FileSystemEvent) -> bool:
        """Check if event should be handled based on patterns"""
        try:
            # Always handle directory events
            if event.is_directory:
                return True
                
            # Check ignore patterns
            if self.ignore_patterns:
                for pattern in self.ignore_patterns:
                    if Path(event.src_path).match(pattern):
                        return False
                        
            # Check include patterns
            if self.patterns:
                for pattern in self.patterns:
                    if Path(event.src_path).match(pattern):
                        return True
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking event patterns: {str(e)}")
            return False 