# -*- coding: utf-8 -*-
from .command import adb_command
import time


def get_device_info() -> dict:
    """Retrieves detailed information about the device."""
    device_info = {
        "Model": adb_command('shell getprop ro.product.model').strip(),
        "Android Version": adb_command('shell getprop ro.build.version.release').strip(),
        "SDK Version": adb_command('shell getprop ro.build.version.sdk').strip(),
        "Device": adb_command('shell getprop ro.product.device').strip(),
        "Manufacturer": adb_command('shell getprop ro.product.manufacturer').strip(),
        "Board": adb_command('shell getprop ro.product.board').strip(),
        "Hardware": adb_command('shell getprop ro.product.hardware').strip(),
        "Serial": adb_command('shell getprop ro.serialno').strip(),
        "Build ID": adb_command('shell getprop ro.build.display.id').strip(),
        "Fingerprint": adb_command('shell getprop ro.build.fingerprint').strip(),
        "Host": adb_command('shell getprop ro.build.host').strip(),
        "Time": adb_command('shell getprop ro.build.date').strip(),
    }
    return device_info


def get_apps() -> list:
    """Gets a list of installed applications on the device.
    :return: List of applications
    """
    
    result = adb_command("shell pm list packages -3")
    return [line.replace('package:', '').strip() for line in result.splitlines() if line]


def run_app(package_name: str):
    """Launches an application by package name.
    :return: class for application control
    """
    app = Application(package_name)
    app.launch()
    return app


def stop_app(package_name) -> None:
    """Stops an application by package name."""
    adb_command(f"shell am force-stop {package_name}")
        
        
class Application:
    def __init__(self, package_name):
        self.package_name = package_name

    def launch(self) -> None:
        """Launches an application"""
        adb_command(f"shell monkey -p {self.package_name} -c android.intent.category.LAUNCHER 1")
        
    def close(self) -> None:
        """Stops the application."""
        adb_command(f"shell am force-stop {self.package_name}")
        
    def restart(self) -> None:
        """Reloads the application."""
        self.close()
        time.sleep(1)
        self.launch()

    def __repr__(self):
        return f"Application(package_name='{self.package_name}')"