from time import sleep
from middleware.modules.no_usb_metadata import get_NoUsbDevice
from middleware.modules.no_usb_metadata import NoUSBDeviceFoundError
if __name__ == '__main__':
    #ometeo_no_usb = NoUsbDevice()
    try:
        mk3_no_usb = get_NoUsbDevice()
        #ometeo_no_usb.micro_reset()
        #sleep(5)
        mk3_no_usb.get_micro_id()
        #ometeo_no_usb.usb_disconnect()
        sleep(1)
        mk3_no_usb.upstream_on()
        sleep(5)
        mk3_no_usb.pc_on()
        sleep(5)
        #mk3_no_usb.device_off()
        print(mk3_no_usb.connection_status())
    except NoUSBDeviceFoundError as err:
        print(err.message)