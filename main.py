from time import sleep
from middleware.modules.no_usb_metadata import NoUsbDevice

if __name__ == '__main__':
    ometeo_no_usb = NoUsbDevice()
    #ometeo_no_usb.micro_reset()
    #sleep(5)
    ometeo_no_usb.get_micro_id()
    ometeo_no_usb.usb_disconnect()
    sleep(5)
    ometeo_no_usb.usb_connect()