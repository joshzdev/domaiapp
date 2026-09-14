"""
DōmAI Monitoring Package
Provides comprehensive monitoring capabilities
"""

from .manager import MonitoringManager
from .network import NetworkMonitor
from .system import SystemMonitor
from .process import ProcessMonitor

__all__ = [
    'MonitoringManager',
    'NetworkMonitor',
    'SystemMonitor',
    'ProcessMonitor'
]

# Version
__version__ = '1.0.0'

# Default monitoring manager instance
_default_manager = None

def get_manager() -> MonitoringManager:
    """Get the default monitoring manager instance"""
    global _default_manager
    if _default_manager is None:
        _default_manager = MonitoringManager()
    return _default_manager 