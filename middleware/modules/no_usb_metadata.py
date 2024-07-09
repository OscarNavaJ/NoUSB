import hid
import json
from time import sleep

from middleware.settings.config import DEVICE_DATA_JSON

class NoUsbDetectHidDevice:
    def __init__(self) -> None:
        self.device = None
        self.device_meta = self._find_device()
    
    def _find_device(self) -> dict:
        device_meta = None
        for hid_device in hid.enumerate():
            if hid_device['manufacturer_string'] == 'NO USB' and hid_device['product_string'] == 'NO USB':
                device_meta = hid_device
                
        try:
            self.device = hid.device()
            self.device.open(device_meta['vendor_id'], device_meta['product_id'])
            self.device.set_nonblocking(0)
            print('Device found and running !\n')
            print(f"Device Information-> \nName: {device_meta['product_string']} \nProduct ID: {device_meta['product_id']} \nVendor ID: {device_meta['vendor_id']}")
        except IOError as ex:
            print(f'An Exception Occurred: {ex}')
            print('Please verify your NO USB device connection !')

        _vendor_id_str = str(device_meta['product_id'])
        with open(DEVICE_DATA_JSON, 'r+') as json_file:
            json_data = json.load(json_file)
            if _vendor_id_str in json_data:
                device_meta.update(json_data[_vendor_id_str])
                #'800006940800'
        return device_meta
        

class NoUsbDevice(NoUsbDetectHidDevice):
    def __init__(self) -> None:
        super().__init__()
        self.major_cmd = self.device_meta['major_command']
        self.info_cmd = 1

    def get_micro_id(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        self._report_transaction((self.info_cmd,))
    def vcc_on(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
            
        self._report_transaction((self.major_cmd, port, 1))
        
    def vcc_off(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
            
        self._report_transaction((self.major_cmd, port, 0))

    def usb_connect(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        self._report_transaction((self.major_cmd, port, 9))
    def usb_disconnect(self, port=None):
        if not self.device_meta['multi_port']:
            port = 1
        self._report_transaction((self.major_cmd, port, 10))

    def micro_reset(self):
        self._report_transaction((self.major_cmd, 1, 99))
    def _report_transaction(self, write_data : tuple):
        self.device.write([1,*write_data] + [0] * 60)
        sleep(0.05)
        while True:
            d = self.device.read(64)
            if d:
                print(d)
                break
            else:
                break