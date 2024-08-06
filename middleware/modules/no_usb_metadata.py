import hid
import json
from time import sleep
from middleware.settings.config import DEVICE_DATA_JSON
from abc import ABC, abstractmethod
from typing import List
import logging

logger = logging.getLogger('HIDLogger')
logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

class NoUSBDeviceFoundError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
class NoUsbDetectHidDevice(ABC):
    def __init__(self,product_id = None, serial_pn = None) -> None:
        self.found = False
        self.device = None
        self.device_meta = self._find_device(product_id = product_id, serial_pn = serial_pn)
        if not self.found:
            raise NoUSBDeviceFoundError("No² USB Found")


    def device_filter(self,device, vendor_id = 'NO USB', product_id = None, serial_pn = None):

        if not device or device['manufacturer_string'] != vendor_id:
            return False


        try:

            self.device = hid.device()
            self.device_meta = device
            self.device_type = self.device_meta['product_string']
            self.device.open_path(device["path"])
            self.device.set_nonblocking(0)

            if product_id and product_id != self.device_meta['product_string']:
                return False

            if device and serial_pn and serial_pn != self.get_micro_id():
                return False

            print('Device found and running !\n')
            logger.debug(f"Device Information-> \nName: {device['product_string']} \nProduct ID: {device['product_id']} \nVendor ID: {device['vendor_id']}")
            logger.debug(f"{device["path"]}")
        except (IOError, TypeError) as ex:
            print('Please verify your NO USB device connection !',ex)
            raise NoUSBDeviceFoundError("No² USB Found")
        self.found = True
        return device

    def get_micro_id(self, port=None):
        id_bytes_list = self._report_transaction((1,))
        response = int(str.join("",[str(i) for i in id_bytes_list]).rstrip("0"))
        return response

    def _report_transaction(self, write_data : tuple):
        self.device.write([1,*write_data] + [0] * 60)
        sleep(0.05)
        response = None
        while True:
            response = self.device.read(64)
            if response:
                logger.debug(response)
                break
            else:
                break
        return response

    def _find_device(self, product_id = None, serial_pn = None) -> dict:

        for hid_device in hid.enumerate():
            if self.device_filter(hid_device,product_id=product_id,serial_pn=serial_pn):
                device_meta = hid_device
                _vendor_id_str = str(device_meta['product_id'])
                with open(DEVICE_DATA_JSON, 'r+') as json_file:
                    json_data = json.load(json_file)
                    if _vendor_id_str in json_data:
                        device_meta.update(json_data[_vendor_id_str])
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
    nousb = None
    hid_device = NoUsbDetectHidDevice(product_id = product_id, serial_pn = serial_pn)
    if hid_device.device_type in ("Not a double host switch","NO USB", "Mk3"):
        nousb = Mk3NoUsbDevice(hid_device)
    elif hid_device.device_type in ("NO USB", "Ometeo", "Mk2"):
        nousb = OmeteoNoUsbDevice(hid_device)
    if not nousb:
        raise NoUSBDeviceFoundError("No² USB Found")
    return nousb
