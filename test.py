#!/usr/bin/env python3
"""
Test suite for debugging screen capture and keyboard control
"""

import sys
import time
from screen_capture import ScreenCapture
from keyboard_controller import RakkRGBController


def test_screen_capture():
    """Test screen capture functionality."""
    print("\n" + "=" * 50)
    print("Testing Screen Capture")
    print("=" * 50)

    try:
        screen = ScreenCapture()
        print("✓ Screen capture initialized")

        print("\nCapturing 5 samples:")
        colors = []
        for i in range(5):
            color = screen.get_average_screen_color()
            colors.append(color)
            print(f"  Sample {i + 1}: RGB({color[0]}, {color[1]}, {color[2]})")
            time.sleep(0.2)

        # Check for variation
        avg_r = sum(c[0] for c in colors) / len(colors)
        avg_g = sum(c[1] for c in colors) / len(colors)
        avg_b = sum(c[2] for c in colors) / len(colors)

        print(f"\nAverage: RGB({int(avg_r)}, {int(avg_g)}, {int(avg_b)})")

        # Check variance
        variance = sum(abs(c[0] - int(avg_r)) + abs(c[1] - int(avg_g)) + abs(c[2] - int(avg_b)) for c in colors) / len(colors)
        print(f"Color variance: {variance:.1f}")

        if variance > 50:
            print("⚠️  High color variance - try moving a window around")
        else:
            print("✓ Screen capture working correctly")

        screen.close()
        return True

    except Exception as e:
        print(f"✗ Screen capture failed: {e}")
        return False


def test_keyboard_connection():
    """Test keyboard connection."""
    print("\n" + "=" * 50)
    print("Testing Keyboard Connection")
    print("=" * 50)

    try:
        keyboard = RakkRGBController()
        print("✓ Keyboard found and connected")
        return keyboard

    except Exception as e:
        print(f"✗ Keyboard connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check that your Rakk Ilis is connected via USB")
        print("2. Run: python3 find_keyboard.py (or with sudo)")
        print("3. Verify USB IDs match in keyboard_controller.py")
        return None


def test_keyboard_colors(keyboard):
    """Test setting colors on keyboard."""
    if keyboard is None:
        print("\n⊘ Skipping keyboard color test (not connected)")
        return

    print("\n" + "=" * 50)
    print("Testing Keyboard Colors")
    print("=" * 50)

    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("Yellow", (255, 255, 0)),
        ("Magenta", (255, 0, 255)),
        ("Cyan", (0, 255, 255)),
        ("White", (255, 255, 255)),
        ("Off", (0, 0, 0)),
    ]

    try:
        for name, (r, g, b) in colors:
            keyboard.set_color(r, g, b)
            print(f"✓ Set to {name}: RGB({r}, {g}, {b})")
            time.sleep(0.3)

        print("\nKeyboard color test completed!")
        keyboard.close()

        # if the keyboard never lit up, offer probe instructions
        print("\nIf the LEDs remained dark, try running the probe routine:")
        print("  >>> from keyboard_controller import RakkRGBController")
        print("  >>> k = RakkRGBController()")
        print("  >>> k.probe_color()  # CTRL+C when you see output")
        return True

    except Exception as e:
        print(f"✗ Color test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n🧪 RGB Controller Test Suite")
    print("=" * 50)

    # Test screen capture
    screen_ok = test_screen_capture()

    # Test keyboard
    keyboard = test_keyboard_connection()

    # Test colors
    if keyboard:
        test_keyboard_colors(keyboard)

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)

    if screen_ok and keyboard:
        print("✓ All tests passed! Ready to run main.py")
        return 0
    elif screen_ok:
        print("⚠️  Screen capture works, but keyboard has issues")
        print("   See troubleshooting above")
        return 1
    else:
        print("⚠️  Screen capture failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
