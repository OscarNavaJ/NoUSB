from __future__ import print_function
from abc import ABC, abstractmethod

import hid
import time
import numpy as np

from device.vendor_data import Vendor
from device.device_data import USBBlenderMK1
# enumerate USB devices

for d in hid.enumerate():
    keys = list(d.keys())
    keys.sort()
    for key in keys:
        print("%s : %s" % (key, d[key]))
    print()

# try opening a device, then perform write and read


class BlenderHIDDevice:
    def __init__(self,product_id):
        self.vendor_id = Vendor.vendor_id
        self.product_id = product_id
        self.device = None

    def get_hid_device(self):
        try:
            self.device = hid.device()
            self.device.open(Vendor.vendor_id.value, self.product_id)
            self.device.set_nonblocking(0)
            print("Manufacturer: %s" % self.device.get_manufacturer_string())
            print("Product: %s" % self.device.get_product_string())
            print("Serial No: %s" % self.device.get_serial_number_string())
        except IOError as ex:
            print(ex)
            print("hid error:")
            print(self.device.error())
            print("")
            print("You probably don't have the hard-coded device.")
            print("Update the h.open() line in this script with the one")
            print("from the enumeration list output above and try again.")
        return self

    @abstractmethod
    def report_transaction(self,write_data):
        pass
    def __del__(self):
        try:
            self.device.close()
        except Exception as err:
            print(err)

class BlenderMK1(BlenderHIDDevice):
    product_id = USBBlenderMK1.product_id
    major_command = USBBlenderMK1.major_command

    def __init__(self):
        BlenderHIDDevice.__init__(self,self.product_id)

    def report_transaction(self,write_data : tuple):
        self.device.write([1,*write_data] + [0] * 60)
        time.sleep(0.05)
        while True:
            d = self.device.read(64)
            if d:
                print(d)
                break
            else:
                break