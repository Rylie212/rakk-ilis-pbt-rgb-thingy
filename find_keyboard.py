#!/usr/bin/env python3
"""
USB Device Scanner - Helps identify Rakk Ilis keyboard USB IDs
"""

import hid


def scan_usb_devices():
    """Scan and display all connected USB HID devices."""
    devices = hid.enumerate()
    
    if not devices:
        print("No USB HID devices found!")
        return

    print("=" * 70)
    print("Connected USB HID Devices:")
    print("=" * 70)
    
    rakk_devices = []
    
    for idx, device in enumerate(devices, 1):
        vendor_id = device['vendor_id']
        product_id = device['product_id']
        manufacturer = device.get('manufacturer_string', 'Unknown')
        product_name = device.get('product_string', 'Unknown')
        
        # Print all devices
        print(f"\n{idx}. Vendor: {manufacturer} | Product: {product_name}")
        print(f"   Vendor ID: {hex(vendor_id)} | Product ID: {hex(product_id)}")
        print(f"   Path: {device.get('path', 'Unknown')}")
        
        # Track Rakk devices
        if "rakk" in manufacturer.lower() or "rakk" in product_name.lower():
            rakk_devices.append({
                'vendor': vendor_id,
                'product': product_id,
                'manufacturer': manufacturer,
                'product_name': product_name,
                'path': device.get('path')
            })
    
    print("\n" + "=" * 70)
    
    if rakk_devices:
        print("✓ Found Rakk Ilis device(s)!")
        for dev in rakk_devices:
            print(f"\n  Device: {dev['product_name']}")
            print(f"  VENDOR_ID = {hex(dev['vendor'])}")
            print(f"  PRODUCT_ID = {hex(dev['product'])}")
            print(f"\n  Update these in keyboard_controller.py:")
            print(f"    VENDOR_ID = {hex(dev['vendor'])}")
            print(f"    PRODUCT_ID = {hex(dev['product'])}")
    else:
        print("⚠️  No Rakk devices found!")
        print("\nMake sure your Rakk Ilis is connected via USB.")
        print("If it's connected, the device might appear under a different vendor name.")
        print("Check the output above for any mechanical keyboard devices.")


if __name__ == "__main__":
    try:
        scan_usb_devices()
    except Exception as e:
        print(f"Error scanning USB devices: {e}")
        print("\nOn Windows, this should work without elevated permissions.")
        print("On Linux/Mac, you may need to run with sudo:")
        print("  sudo python3 find_keyboard.py")
