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

        # Try each HID interface until one accepts a color write.  This
        # heuristics helps when the correct interface isn't the keyboard
        # endpoint (many SONiX boards expose several, e.g. Col02/Col03 ...).
        device_info = None
        for d in devices:
            try:
                dev = hid.device()
                if d.get("path"):
                    dev.open_path(d["path"])
                else:
                    dev.open(self.VENDOR_ID, self.PRODUCT_ID)
                dev.set_nonblocking(1)

                # perform a harmless write (black).  If the interface rejects
                # it or returns 0 bytes written we assume it's not the RGB
                # endpoint.
                try:
                    ret = dev.write(bytes([0x08, 0x01, 0x01, 0, 0, 0, 0, 0]))
                except Exception:
                    ret = 0

                if ret:
                    device_info = d
                    self.device = dev
                    break
                else:
                    dev.close()
            except Exception:
                # ignore and try next
                continue

        # if probing failed, fall back to the first device (previous logic)
        if device_info is None:
            device_info = devices[0]
            self.device = hid.device()
            if device_info.get("path"):
                self.device.open_path(device_info["path"])
            else:
                self.device.open(self.VENDOR_ID, self.PRODUCT_ID)
            self.device.set_nonblocking(1)

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

        # Build a list of candidate packets.  We'll try different report IDs
        # and also pad to the typical 64-byte HID report size, since many SONiX
        # controllers expect full‑length reports.
        candidates = []
        base = [0x08, 0x01, 0x01, r, g, b, 0x00, 0x00]
        # no prefix
        candidates.append(base)
        # common zero prefix
        candidates.append([0x00] + base)
        # alternate header values seen in some firmwares
        candidates.append([0x08, 0x05, 0x01, r, g, b, 0x00, 0x00])
        candidates.append([0x00, 0x08, 0x05, 0x01, r, g, b, 0x00, 0x00])
        # try explicit report IDs 1..4
        for rid in range(1, 5):
            candidates.append([rid] + base)
            candidates.append([rid, 0x00] + base)

        # each candidate should also be tried as a 64-byte packet
        expanded = []
        for cmd in candidates:
            expanded.append(cmd)
            if len(cmd) < 64:
                expanded.append(cmd + [0] * (64 - len(cmd)))
        candidates = expanded

        for idx, cmd in enumerate(candidates, 1):
            data = bytes(cmd)
            try:
                written = self.device.write(data)
                print(f"DEBUG: write attempt {idx} len={len(cmd)} cmd={cmd[:16]}... returned={written}")
                if written:
                    return
            except Exception as e:
                print(f"DEBUG: write attempt {idx} raised {e}")

            # try feature report as alternative path
            try:
                fed = self.device.send_feature_report(data)
                print(f"DEBUG: feature attempt {idx} len={len(cmd)} cmd={cmd[:16]}... returned={fed}")
                if fed:
                    return
            except Exception as e:
                print(f"DEBUG: feature attempt {idx} raised {e}")

        # if we reach here nothing seemed to work
        print("Warning: all color write/feature attempts returned 0 or failed")

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

    def probe_color(self):
        """Try a series of commands while user watches keyboard.

        Useful when the exact HID report format is unknown.  Each attempt
        will be printed with its contents; press CTRL+C to abort once you
        see your keyboard respond.
        """
        print("Probing color commands; watch the keyboard and interrupt when it lights up...")
        r, g, b = 255, 0, 0
        base = [0x08, 0x01, 0x01, r, g, b, 0x00, 0x00]
        # build a few variants with different report IDs and padding
        candidates = [base, [0x00] + base,
                      [0x08, 0x05, 0x01, r, g, b, 0x00, 0x00],
                      [0x00, 0x08, 0x05, 0x01, r, g, b, 0x00, 0x00]]
        for rid in range(1, 5):
            candidates.append([rid] + base)
            candidates.append([rid, 0x00] + base)
        # include padded 64‑byte versions
        padded = []
        for cmd in candidates:
            padded.append(cmd)
            if len(cmd) < 64:
                padded.append(cmd + [0] * (64 - len(cmd)))
        candidates = padded

        try:
            while True:
                for idx, cmd in enumerate(candidates, 1):
                    try:
                        written = self.device.write(bytes(cmd))
                        print(f"probe {idx} len={len(cmd)} -> {written}")
                    except Exception as e:
                        print(f"probe {idx} error: {e}")
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("Probe stopped")
