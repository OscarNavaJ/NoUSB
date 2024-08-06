from time import sleep
from middleware.modules.no_usb_metadata import get_NoUsbDevice
from middleware.modules.no_usb_metadata import NoUSBDeviceFoundError
if __name__ == '__main__':
    #ometeo_no_usb = NoUsbDevice()
    try:
        no_usb_mk3_A = get_NoUsbDevice(serial_pn=4215205202187218754535432,product_id="Not a double host switch")
        no_usb_mk3_B = get_NoUsbDevice(serial_pn=4215405402187218754535432,product_id="Not a double host switch")

        no_usb_mk3_A.device_off()
        no_usb_mk3_B.device_off()
        sleep(5)
        no_usb_mk3_A.pc_on()
        no_usb_mk3_B.pc_on()
        sleep(5)
        no_usb_mk3_A.device_off()
        no_usb_mk3_B.device_off()
        #ometeo_no_usb.micro_reset()
        #sleep(5)
        # print(mk3_no_usb.get_micro_id())
        # mk3_no_usb.device_off()
        # sleep(1)
        # mk3_no_usb.upstream_on()
        # sleep(5)
        # mk3_no_usb.device_off()
        # sleep(5)
        # mk3_no_usb.pc_on()
        # sleep(5)

        #print(no_usb_mk3_A.connection_status())
    except NoUSBDeviceFoundError as err:
        print(err.message)