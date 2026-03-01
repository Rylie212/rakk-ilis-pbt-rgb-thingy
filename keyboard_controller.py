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
        """Find and connect to the Rakk Ilis keyboard.

        Some Rakk boards expose multiple HID interfaces; the RGB controller
        is usually on the keyboard interface (ends with "\\KBD" in the path).
        If we just open by vendor/product the wrong endpoint may be chosen and
        writes will silently be ignored, leaving the backlight dark.
        """
        # Enumerate all HID devices with our VID/PID
        devices = hid.enumerate(self.VENDOR_ID, self.PRODUCT_ID)

        if not devices:
            raise RuntimeError(
                f"Rakk Ilis keyboard not found. "
                f"Expected Vendor ID: {hex(self.VENDOR_ID)}, "
                f"Product ID: {hex(self.PRODUCT_ID)}"
            )

        # Prefer the device whose path contains "kbd" (keyboard interface)
        device_info = None
        for d in devices:
            path = d.get("path", "").lower()
            if "kbd" in path:
                device_info = d
                break

        # fallback to first entry if nothing obvious
        if device_info is None:
            device_info = devices[0]

        try:
            self.device = hid.device()

            # open using the explicit path so we don't accidentally hit a
            # non-RGB interface when multiple handlers exist.
            if device_info.get("path"):
                self.device.open_path(device_info["path"])
            else:
                self.device.open(self.VENDOR_ID, self.PRODUCT_ID)

            # Set non-blocking mode for better responsiveness
            self.device.set_nonblocking(1)

        except OSError as e:
            raise RuntimeError(f"Failed to open HID device: {e}")

        print(f"✓ Rakk Ilis keyboard connected")
        print(f"  Device: {device_info.get('product_string', 'Unknown')}")
        print(f"  Path: {device_info.get('path', 'Unknown')}")

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
            # Try common RGB command structure. Some SONiX boards expect a
            # leading report ID (0x00) while others do not; try both.
            command = [0x08, 0x01, 0x01, r, g, b, 0x00, 0x00]
            written = self.device.write(bytes(command))
            if written == 0:
                # maybe needs an extra 0 prefix
                command = [0x00] + command
                written = self.device.write(bytes(command))
            if written == 0:
                print("Warning: HID write returned 0 bytes written; the device
may not support this report format")
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
