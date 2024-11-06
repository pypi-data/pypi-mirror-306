import subprocess

device_id = None


def adb_command(command, shell=True, capture_output=True, text=True) -> str:
    """Method for executing an ADB command and returning the result."""
    
    if not device_id:
        result = subprocess.run(f"adb {command}", shell=shell, capture_output=capture_output, text=text)
    else:
        result = subprocess.run(f"adb -s {device_id} {command}", shell=shell, capture_output=capture_output, text=text)
        
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        raise RuntimeError(f"ADB command failed: {result.stderr.strip()}")
    
    
def set_device(device):
    global device_id
    device_id = device