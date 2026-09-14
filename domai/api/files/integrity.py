"""
File integrity monitoring module
Handles file integrity checking and verification
"""

import logging
import hashlib
import os
import stat
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from datetime import datetime

class IntegrityMonitor:
    """Monitor file integrity and changes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_file_hash(self, path: str, algorithm: str = "sha256") -> Optional[str]:
        """Calculate file hash using specified algorithm"""
        try:
            hash_func = getattr(hashlib, algorithm)()
            path_obj = Path(path)
            
            if not path_obj.is_file():
                raise ValueError(f"Not a file: {path}")
                
            # Read file in chunks to handle large files
            with open(path_obj, "rb") as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
                    
            return hash_func.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Error calculating file hash: {str(e)}")
            return None
            
    def get_file_metadata(self, path: str) -> Dict[str, Any]:
        """Get file metadata including permissions and timestamps"""
        try:
            path_obj = Path(path)
            stat_result = path_obj.stat()
            
            return {
                "size": stat_result.st_size,
                "mode": stat_result.st_mode,
                "uid": stat_result.st_uid,
                "gid": stat_result.st_gid,
                "atime": datetime.fromtimestamp(stat_result.st_atime),
                "mtime": datetime.fromtimestamp(stat_result.st_mtime),
                "ctime": datetime.fromtimestamp(stat_result.st_ctime),
                "permissions": stat.filemode(stat_result.st_mode),
                "type": self._get_file_type(stat_result.st_mode)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file metadata: {str(e)}")
            return {}
            
    def verify_signature(self, path: str, signature: str) -> bool:
        """Verify file signature"""
        try:
            calculated_hash = self.calculate_file_hash(path)
            return calculated_hash == signature
            
        except Exception as e:
            self.logger.error(f"Error verifying signature: {str(e)}")
            return False
            
    def scan_directory(self, directory: str, recursive: bool = True) -> Dict[str, Dict[str, Any]]:
        """Scan directory for file integrity information"""
        results = {}
        try:
            path_obj = Path(directory)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {directory}")
                
            # Get list of files
            if recursive:
                files = path_obj.rglob("*")
            else:
                files = path_obj.glob("*")
                
            # Process each file
            for file_path in files:
                if file_path.is_file():
                    try:
                        relative_path = str(file_path.relative_to(path_obj))
                        results[relative_path] = {
                            "hash": self.calculate_file_hash(str(file_path)),
                            "metadata": self.get_file_metadata(str(file_path))
                        }
                    except Exception as e:
                        self.logger.error(f"Error processing file {file_path}: {str(e)}")
                        continue
                        
        except Exception as e:
            self.logger.error(f"Error scanning directory: {str(e)}")
            
        return results
        
    def compare_snapshots(self, 
                         snapshot1: Dict[str, Dict[str, Any]], 
                         snapshot2: Dict[str, Dict[str, Any]]
                         ) -> Dict[str, List[str]]:
        """Compare two snapshots and return differences"""
        changes = {
            "added": [],
            "removed": [],
            "modified": [],
            "unchanged": []
        }
        
        try:
            # Get sets of files
            files1 = set(snapshot1.keys())
            files2 = set(snapshot2.keys())
            
            # Find added and removed files
            changes["added"] = list(files2 - files1)
            changes["removed"] = list(files1 - files2)
            
            # Check for modifications in common files
            common_files = files1 & files2
            for file in common_files:
                if snapshot1[file]["hash"] != snapshot2[file]["hash"]:
                    changes["modified"].append(file)
                else:
                    changes["unchanged"].append(file)
                    
        except Exception as e:
            self.logger.error(f"Error comparing snapshots: {str(e)}")
            
        return changes
        
    def monitor_critical_files(self, paths: List[str]) -> Dict[str, Dict[str, Any]]:
        """Monitor specific critical files"""
        results = {}
        
        try:
            for path in paths:
                path_obj = Path(path)
                if path_obj.exists():
                    results[path] = {
                        "hash": self.calculate_file_hash(path),
                        "metadata": self.get_file_metadata(path),
                        "exists": True
                    }
                else:
                    results[path] = {
                        "exists": False,
                        "error": "File not found"
                    }
                    
        except Exception as e:
            self.logger.error(f"Error monitoring critical files: {str(e)}")
            
        return results
        
    def _get_file_type(self, mode: int) -> str:
        """Determine file type from mode"""
        if stat.S_ISREG(mode):
            return "regular"
        elif stat.S_ISDIR(mode):
            return "directory"
        elif stat.S_ISLNK(mode):
            return "symlink"
        elif stat.S_ISFIFO(mode):
            return "fifo"
        elif stat.S_ISSOCK(mode):
            return "socket"
        elif stat.S_ISBLK(mode):
            return "block"
        elif stat.S_ISCHR(mode):
            return "character"
        else:
            return "unknown" 