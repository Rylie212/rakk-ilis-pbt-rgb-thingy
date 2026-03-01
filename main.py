#!/usr/bin/env python3
"""
Rakk Ilis RGB Screen Sync
Continuously samples your screen color and syncs it to your keyboard RGB.
"""

import time
import sys
from screen_capture import ScreenCapture
from keyboard_controller import RakkRGBController


def main():
    """Main loop for RGB sync."""
    print("🎮 Rakk Ilis RGB Screen Sync")
    print("=" * 40)

    # Initialize components
    try:
        print("Initializing screen capture...")
        screen = ScreenCapture()
        print("✓ Screen capture ready")
    except Exception as e:
        print(f"✗ Screen capture failed: {e}")
        return 1

    try:
        print("Connecting to keyboard...")
        keyboard = RakkRGBController()
    except Exception as e:
        print(f"✗ Keyboard connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Rakk Ilis is connected via USB")
        print("2. Check if you have sufficient USB permissions")
        print("3. Try running with: sudo python3 main.py")
        print("\nYou may need to:")
        print("- Find your keyboard's USB Vendor/Product ID using: lsusb")
        print("- Update VENDOR_ID and PRODUCT_ID in keyboard_controller.py")
        return 1

    print("\n" + "=" * 40)
    print("🟢 Starting RGB sync (Ctrl+C to stop)")
    print("=" * 40)

    try:
        update_count = 0
        last_color = None

        while True:
            # Get screen color
            try:
                color = screen.get_average_screen_color()
            except Exception as e:
                print(f"Screen capture error: {e}")
                time.sleep(0.1)
                continue

            # Only update if color changed significantly
            # (reduces USB load and flicker)
            if last_color is None or color_distance(last_color, color) > 5:
                try:
                    keyboard.set_color(*color)
                    last_color = color
                    update_count += 1

                    # Print status every 60 updates (~1-2 seconds at fast polling)
                    if update_count % 60 == 0:
                        print(f"RGB: ({color[0]}, {color[1]}, {color[2]})")

                except Exception as e:
                    print(f"Keyboard error: {e}")
                    keyboard.close()
                    break

            # Small sleep to avoid 100% CPU
            time.sleep(0.016)  # ~60 FPS sampling

    except KeyboardInterrupt:
        print("\n\n⏹  Stopping RGB sync...")
    finally:
        try:
            keyboard.close()
            screen.close()
            print("✓ Resources cleaned up")
        except:
            pass

    return 0


def color_distance(color1, color2):
    """
    Calculate perceptual color distance using Euclidean distance.
    
    Args:
        color1, color2: (R, G, B) tuples
        
    Returns:
        float: Distance between colors
    """
    # Weight colors by human perception
    # Green is brighter to human eyes
    r_diff = (color1[0] - color2[0]) * 0.299
    g_diff = (color1[1] - color2[1]) * 0.587
    b_diff = (color1[2] - color2[2]) * 0.114

    return (r_diff ** 2 + g_diff ** 2 + b_diff ** 2) ** 0.5


if __name__ == "__main__":
    sys.exit(main())
