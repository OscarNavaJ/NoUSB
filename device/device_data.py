from dataclasses import dataclass

@dataclass
class USBBlender:
    product_id : int
    ports_number : int
    start_port : int
    major_command : int


USBBlenderMK1 = USBBlender(
    product_id = 22352,
    ports_number = 3,
    start_port = 2,
    major_command = 10
)