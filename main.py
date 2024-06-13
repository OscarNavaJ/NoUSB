"""
author: Oscar Nava

"""

from device.device_hid import BlenderMK1

blender_mk1 = BlenderMK1()
device_mk1 = blender_mk1.get_hid_device()
device_mk1.report_transaction((1,2,2))