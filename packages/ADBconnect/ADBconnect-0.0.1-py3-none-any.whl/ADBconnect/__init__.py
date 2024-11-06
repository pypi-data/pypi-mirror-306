import shutil

from .command import set_device
from .control import *
from .screen import *
from .action import *
from .servis import *


class Phone:
    def __init__(self, adb_path=None, device=None):
        
        if device:
            set_device(device)
            
        if adb_path:
            os.environ['PATH'] += os.pathsep + adb_path

        if not shutil.which("adb"):
            raise EnvironmentError("ADB not found. Make sure ADB is installed and added to PATH.")
        
        
__all__ = ["Phone"]