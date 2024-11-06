# -*- coding: utf-8 -*-
from .command import adb_command


def tap(x: int, y: int) -> None:
	"""Clicks on the screen at the specified coordinates."""
	adb_command(f"shell input tap {x} {y}")


def swipe(start_x: int, start_y: int, end_x: int, end_y: int, duration=999) -> None:
	"""swipe from one place to another."""
	adb_command(f"shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}")
	
	
def input_text(text: str) -> None:
	"""Enter some message into the text field for input."""
	adb_command(f'shell input text "{text.replace(" ", "%s")}"')
	
	
def screen() -> None:
	"""Turns phone screen on or off."""
	adb_command("shell input keyevent 26")
	

def reboot() -> None:
	"""Reboot phone."""
	adb_command("shell reboot")
	
	
def power_off() -> None:
	"""Reboot phone."""
	adb_command("shell reboot -p")
	
	
def toast(message: str) -> None:
	"""Display a message on the screen."""
	adb_command(f'shell settings put global toast "{message}"')
	
	
def send_notification(text):
    """Sends a notification to the device with the specified text."""
    command = f'shell cmd notification post default_channel {text}'
    adb_command(command)
	

def set_brightness(value: int) -> None:
    """Sets the screen brightness (from 0 to 255)."""
    if 0 <= value <= 255:
        adb_command(f'shell settings put system screen_brightness {value}')
    else:
        raise ValueError("Brightness should be between 0 and 255.")
	
	
def set_volume(volume: int) -> None:
    """Sets the sound level (from 0 to 15)."""
    if 0 <= volume <= 15:
        adb_command(f'shell media volume --set {volume}')
    else:
        raise ValueError("The sound level should be between 0 and 15.")