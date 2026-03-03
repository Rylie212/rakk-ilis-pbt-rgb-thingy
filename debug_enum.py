import hid
from keyboard_controller import RakkRGBController

print('Enumerating devices')
devs = hid.enumerate(RakkRGBController.VENDOR_ID, RakkRGBController.PRODUCT_ID)
print(f'Found {len(devs)} entries:')
for d in devs:
    print(d)
