import hid
import json
from time import sleep
from middleware.settings.config import DEVICE_DATA_JSON
from abc import ABC, abstractmethod
from typing import List

class NoUSBDeviceFoundError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
class NoUsbDetectHidDevice(ABC):
    def __init__(self) -> None:
        self.device = None
        self.device_meta = self._find_device()
        self.device_type = self.device_meta['product_string']

    def device_filter(self,device, vendor_id = 'NO USB', product_id = None, serial_pn = None):
        if not device or device['manufacturer_string'] != vendor_id:
            return False
        if product_id and product_id != device['product_string']:
            return False
        if serial_pn and product_id != self.get_micro_id():
            return False
        return True

    def get_micro_id(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.info_cmd,))
        return response

    def _report_transaction(self, write_data : tuple):
        self.device.write([1,*write_data] + [0] * 60)
        sleep(0.05)
        response = None
        while True:
            response = self.device.read(64)
            if response:
                print(response)
                break
            else:
                break
        return response

    def _find_device(self, product_id = None, serial_pn = None) -> dict:
        device_meta = None
        for hid_device in list(filter(lambda x:self.device_filter(x,product_id=product_id,serial_pn=serial_pn),hid.enumerate())):
            # if hid_device['manufacturer_string'] == 'NO USB' and hid_device['product_string'] == 'NO USB':
            device_meta = hid_device

                
        try:
            self.device = hid.device()
            self.device.open(device_meta['vendor_id'], device_meta['product_id'])
            self.device.set_nonblocking(0)
            print('Device found and running !\n')
            print(f"Device Information-> \nName: {device_meta['product_string']} \nProduct ID: {device_meta['product_id']} \nVendor ID: {device_meta['vendor_id']}")
        except (IOError, TypeError) as ex:
            print('Please verify your NO USB device connection !')
            raise NoUSBDeviceFoundError("No² USB Found")
        _vendor_id_str = str(device_meta['product_id'])
        with open(DEVICE_DATA_JSON, 'r+') as json_file:
            json_data = json.load(json_file)
            if _vendor_id_str in json_data:
                device_meta.update(json_data[_vendor_id_str])
                #'800006940800'
        return device_meta
        

class OmeteoNoUsbDevice(NoUsbDetectHidDevice):
    def __init__(self,hid_device) -> None:
        #super().__init__()
        self.device = hid_device.device
        self.device_meta = hid_device.device_meta
        self.major_cmd = self.device_meta['major_command']
        self.info_cmd = 1
    def vcc_on(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
            
        response = self._report_transaction((self.major_cmd, port, 1))
        return response
        
    def vcc_off(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
            
        response = self._report_transaction((self.major_cmd, port, 0))
        return response

    def usb_connect(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.major_cmd, port, 9))
        return response
    def usb_disconnect(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.major_cmd, port, 10))
        return response
    def connection_status(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.major_cmd, port, 11))
        return response

    def micro_reset(self):
        response = self._report_transaction((self.major_cmd, 1, 99))
        return response

class Mk3NoUsbDevice(NoUsbDetectHidDevice):
    def __init__(self,hid_device) -> None:
        #super().__init__()
        self.device = hid_device.device
        self.device_meta = hid_device.device_meta
        self.major_cmd = self.device_meta['major_command']
        self.info_cmd = 1

    def upstream_on(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.major_cmd, port, 8))
        return response

    def device_off(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.major_cmd, port, 9))
        return response

    def pc_on(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.major_cmd, port, 10))
        return response

    def connection_status(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        response = self._report_transaction((self.major_cmd, port, 11))
        return response

    def micro_reset(self):
        response = self._report_transaction((self.major_cmd, 1, 99))
        return response

def get_NoUsbDevice( product_id = None, serial_pn = None):
    hid_device = NoUsbDetectHidDevice()
    nousb = None
    if hid_device.device_type in ("Not a double host switch","NO USB", "Mk3"):
        nousb = Mk3NoUsbDevice(hid_device)
    elif hid_device.device_type in ("NO USB", "Ometeo", "Mk2"):
        nousb = OmeteoNoUsbDevice(hid_device)
    return nousb
