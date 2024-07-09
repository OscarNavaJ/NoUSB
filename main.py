from time import sleep
from middleware.modules.no_usb_metadata import NoUsbDevice

if __name__ == '__main__':
    ometeo_no_usb = NoUsbDevice()
    ometeo_no_usb.vcc_on()
    sleep(5)
    ometeo_no_usb.vcc_off()