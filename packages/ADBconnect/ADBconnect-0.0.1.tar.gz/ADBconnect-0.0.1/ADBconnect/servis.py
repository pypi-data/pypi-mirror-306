# -*- coding: utf-8 -*-
from .command import adb_command


def wifi(enable: bool) -> None:
	"""Turns Wi-Fi on or off."""
	if enable:
		adb_command("shell svc wifi enable")
	else:
		adb_command("shell svc wifi disable")
	
	
def set_proxy(ip: str, port: int) -> None:
	"""enable proxy for phone
	:param ip: Proxy server ip address.
	:param port: Server proxy port.
	"""
	adb_command(f"shell settings put global http_proxy {ip}:{port}")
	
	
def reset_proxy() -> None:
	"""reset proxy settings"""
	adb_command(f"shell settings put global http_proxy :0")


def bluetooth(enable: bool) -> None:
	"""Turns Bluetooth on or off."""
	if enable:
		adb_command("shell service call bluetooth_manager 6")
	else:
		adb_command("shell service call bluetooth_manager 8")


def airplane_mode(enable: bool) -> None:
	"""Turns airplane mode on or off."""
	if enable:
		adb_command("shell settings put global airplane_mode_on 1")
		adb_command("shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true")
	else:
		adb_command("shell settings put global airplane_mode_on 0")
		adb_command("shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false")


def mobile_data(enable: bool) -> None:
	"""Disables mobile network data transmission on the device."""
	if enable:
		adb_command("shell svc data enable")
	else:
		adb_command("shell svc data disable")