# Rakk Ilis PBT RGB Screen Sync

A real-time RGB controller for the Rakk Ilis mechanical keyboard that samples your screen color and syncs it to the keyboard's backlighting—like those fancy LED strips behind your TV!

**Works on Windows, macOS, and Linux!** 🖥️🍎🐧

> **Windows users:** See [WINDOWS_QUICKSTART.md](WINDOWS_QUICKSTART.md) for a quick setup guide!

## Features

✨ **Screen Color Sampling**: Continuously captures the average color of your entire screen  
⚡ **Real-time Sync**: Updates keyboard RGB with minimal latency (~60 FPS)  
🎨 **Smooth Transitions**: Optional color smoothing for less jarring changes  
🔄 **Adaptive Updates**: Only updates when color changes significantly, reducing USB load  

## Requirements

- **Rakk Ilis PBT Mechanical Keyboard**
- **Linux** (Ubuntu/Debian not tested)
- **Python 3.7+**
- USB permissions for HID devices

## Installation

### On Linux

1. **Clone and enter the repo:**
   ```bash
   cd /workspaces/rakk-ilis-pbt-rgb-thingy
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Identify your keyboard's USB IDs:**
   ```bash
   lsusb
   ```
   Look for an entry like `Rakk` or `3151:...`. Note the Vendor ID and Product ID.

4. **Update keyboard IDs (if needed):**
   If the default IDs don't match yours, edit [keyboard_controller.py](keyboard_controller.py):
   ```python
   VENDOR_ID = 0x3151  # Your vendor ID
   PRODUCT_ID = 0x4154  # Your product ID
   ```

### On Windows

1. **Clone and enter the repo:**
   ```bash
   cd \Users\YourUsername\Documents\rakk-ilis-pbt-rgb-thingy
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Identify your keyboard's USB IDs:**
   ```bash
   python find_keyboard.py
   ```
   This will list all USB HID devices. Look for your Rakk Ilis.

4. **Update keyboard IDs (if needed):**
   If the script finds your keyboard but with different IDs, edit [keyboard_controller.py](keyboard_controller.py):
   ```python
   VENDOR_ID = 0x3151  # Your vendor ID
   PRODUCT_ID = 0x4154  # Your product ID
   ```

### On macOS

1. **Clone and enter the repo:**
   ```bash
   cd ~/Documents/rakk-ilis-pbt-rgb-thingy
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Identify your keyboard:**
   ```bash
   python3 find_keyboard.py
   ```

4. **Update keyboard IDs if needed** (same as Linux/Windows above)

## Usage

### Quick Start - Linux/macOS

```bash
# Basic usage
python3 main.py

# With sudo (required if you get permission errors)
sudo python3 main.py
```

### Quick Start - Windows

```bash
# Just run it directly (no sudo needed)
python main.py
```

The script will:
1. Initialize screen capture
2. Connect to your Rakk Ilis
3. Start sampling screen color and syncing RGB
4. Press `Ctrl+C` to stop

### Example Output

```
🎮 Rakk Ilis RGB Screen Sync
========================================
Initializing screen capture...
✓ Screen capture ready
Connecting to keyboard...
✓ Rakk Ilis keyboard connected

========================================
🟢 Starting RGB sync (Ctrl+C to stop)
========================================
RGB: (245, 120, 80)
RGB: (243, 115, 78)
```

## Troubleshooting

### General Issues

**Keyboard not found**

1. **Verify connection:** Make sure your Rakk Ilis is connected via USB
2. **Check USB IDs:** Run `python find_keyboard.py` (Windows) or `python3 find_keyboard.py` (Linux/macOS)
3. **Verify IDs match:** Make sure `VENDOR_ID` and `PRODUCT_ID` in [keyboard_controller.py](keyboard_controller.py) match your device
4. **Common Rakk Ilis IDs:**
   - Vendor: `0x3151`
   - Product: `0x4154` (adjust if different)

**No color changes observed**

- Try moving a bright window across your screen to test
- Check that the keyboard supports RGB control via HID
- Ensure no other RGB software is conflicting with this

### Linux-Specific Issues

**"Permission denied" or USB errors**

You may need USB permissions. Either:

**Option 1: Run with sudo**
```bash
sudo python3 main.py
```

**Option 2: Add udev rules** (permanent solution)
```bash
sudo nano /etc/udev/rules.d/99-rakk-ilis.rules
```

Add this line:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="3151", MODE="0666"
```

Then reload rules:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### Windows-Specific Issues

**"hidapi not found" error**

Make sure you installed the package correctly:
```bash
pip install --upgrade hidapi
```

**Device permissions**

Windows handles HID devices better than Linux - try:
1. Reconnecting the keyboard
2. Running `python find_keyboard.py` again to rescan
3. Restarting the application

**RGB still doesn't work**

The official Rakk software might be blocking the HID interface. Try:
1. Closing any official Rakk RGB control software

If the keyboard connects but the LEDs remain dark:

- **Multiple HID interfaces**: Some boards expose a generic SONiX vendor interface plus a
  separate keyboard interface (paths end with `\\KBD`).  The sync script will now
  automatically pick the `KBD` path, but you can double-check by running
  `python find_keyboard.py` and verifying the `Path:` shown for your device.
- **Report format mismatch**: The code sends a simple eight‑byte packet and retries
  with a leading `0x00` byte.  If neither works you can experiment manually:
  open a Python REPL and use `hid.device().write(...)` or
  `hid.device().send_feature_report(...)` with different byte sequences until you
  see activity.  The debug output prints a warning if zero bytes are written.


2. Unplugging the keyboard, waiting 3 seconds, and plugging it back in
3. Restarting the Python application

### macOS-Specific Issues

**"hidapi.hid_enumerate() failed"**

Make sure hidapi is installed: ```bash
pip install --upgrade hidapi
```

**Device permissions on Big Sur+**

You may need to allow Python universal binary permissions. Try running with sudo:
```bash
sudo python3 main.py
```

## Project Structure

```
.
├── main.py                  # Main controller loop
├── screen_capture.py        # Screen color sampling
├── keyboard_controller.py   # RGB command interface
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## How It Works

1. **Screen Capture**: Uses `mss` for fast screenshot capture (↑60 FPS)
2. **Color Analysis**: Calculates average RGB across all pixels (optimized with NumPy)
3. **RGB Control**: Sends HID commands to keyboard to set color
4. **Smart Updates**: Only sends new color when delta > 5 to reduce flicker/lag

## Performance

- **CPU**: ~2-5% (light sampling + analysis)
- **USB**: Minimal (smart update filtering)
- **Latency**: ~16ms per frame at 60 FPS
- **Screen Impact**: None (doesn't modify display)

## Future Ideas

- [ ] Per-zone RGB control (if keyboard supports it)
- [ ] Custom sampling regions (corners, edges like real TV backlights)
- [ ] Configuration file for smoothing, update rates, and color mapping
- [ ] Keyboard profile support (different behaviors for different apps)
- [ ] Color math adjustments (brightness, saturation, hue rotation)

## License

Open source - feel free to modify and extend!

## Contributing

Found a bug or have a feature idea? Open an issue or submit a PR!
