#!/usr/bin/env python3
"""Utility to brute-force USB control transfers for Rakk Ilis keyboard.

Run this when the official Rakk/SONiX RGB utility is *not* running and watch
your keyboard's LEDs; the script will try every plausible vendor request and
print the results.  CTRL+C to stop when you see a change.

Example:
    python usb_probe.py
"""

import usb.core
import sys

VENDOR_ID = 0x0c45
PRODUCT_ID = 0x8006

# colour to send (red by default)
R, G, B = 255, 0, 0

payload = [0x08, 0x01, 0x01, R, G, B, 0x00, 0x00]

def main():
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        print("Device not found.  Is the keyboard plugged in?")
        sys.exit(1)

    dev.set_configuration()

    print("Starting control transfer probe; press CTRL+C when the keyboard responds")
    try:
        for bm in range(0x20, 0x40):
            for br in range(0x00, 0x10):
                try:
                    ret = dev.ctrl_transfer(bm, br, 0, 0, payload)
                    print(f"ctrl bm=0x{bm:02x} req=0x{br:02x} -> {ret}")
                except Exception as e:
                    print(f"ctrl bm=0x{bm:02x} req=0x{br:02x} error: {e}")
    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == '__main__':
    main()
