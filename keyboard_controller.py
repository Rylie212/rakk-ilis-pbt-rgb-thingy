"""RGB controller for Rakk Ilis mechanical keyboard."""

import hid
import time
import platform


class RakkRGBController:
    """Controls RGB lighting on Rakk Ilis keyboard via USB HID."""

    # USB Vendor ID and Product ID for Rakk Ilis
    # These are common IDs - may need adjustment based on your specific device
    VENDOR_ID = 0x0c45  # SONiX (Rakk Ilis uses SONiX controller)
    PRODUCT_ID = 0x8006  # Rakk Ilis product ID

    def __init__(self):
        """Initialize the RGB controller and find the keyboard."""
        self.device = None
        self.os_name = platform.system()
        self.find_device()

    def find_device(self):
        """Find and connect to the Rakk Ilis keyboard."""
        # Enumerate all HID devices
        devices = hid.enumerate(self.VENDOR_ID, self.PRODUCT_ID)

        if not devices:
            raise RuntimeError(
                f"Rakk Ilis keyboard not found. "
                f"Expected Vendor ID: {hex(self.VENDOR_ID)}, "
                f"Product ID: {hex(self.PRODUCT_ID)}"
            )

        # Try to connect to the first matching device
        device_info = devices[0]
        
        try:
            self.device = hid.device()
            self.device.open(self.VENDOR_ID, self.PRODUCT_ID)
            
            # Set non-blocking mode for better responsiveness
            self.device.set_nonblocking(1)
            
        except OSError as e:
            raise RuntimeError(f"Failed to open HID device: {e}")

        print(f"✓ Rakk Ilis keyboard connected")
        print(f"  Device: {device_info.get('product_string', 'Unknown')}")
        print(f"  Path: {device_info.get('path', 'Unknown')}")

    def set_color(self, r, g, b):
        """
        Set the RGB color on the keyboard.
        
        Args:
            r, g, b: Color values 0-255
        """
        if self.device is None:
            raise RuntimeError("Device not connected")

        # Clamp values to 0-255
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        # Standard RGB HID control command for mechanical keyboards
        # Format: [header] [mode] [frame/color data]
        # This command sets static color
        try:
            # Try common RGB command structure
            command = [0x08, 0x01, 0x01, r, g, b, 0x00, 0x00]
            self.device.write(bytes(command))
        except OSError as e:
            print(f"Warning: HID error sending color - {e}")

    def set_color_smooth(self, r, g, b, steps=30):
        """
        Smoothly transition to a new color.
        
        Args:
            r, g, b: Target color values 0-255
            steps: Number of transition steps
        """
        if self.device is None:
            raise RuntimeError("Device not connected")

        # Get current color (if trackable) or assume black
        current = (0, 0, 0)

        for step in range(steps):
            progress = step / steps
            new_r = int(current[0] + (r - current[0]) * progress)
            new_g = int(current[1] + (g - current[1]) * progress)
            new_b = int(current[2] + (b - current[2]) * progress)

            self.set_color(new_r, new_g, new_b)
            time.sleep(0.01)  # Small delay between steps

    def close(self):
        """Close the USB connection."""
        if self.device:
            try:
                self.device.close()
            except:
                pass
