# Windows Quick Start Guide

## Prerequisites

- **Python 3.7+** - Download from https://www.python.org/downloads/
  - ⚠️ **Important:** Check "Add Python to PATH" during installation
- **Rakk Ilis keyboard** connected via USB

## Setup

1. **Open Command Prompt or PowerShell** in the project folder

2. **Run the setup script:**
   ```bash
   python setup.bat
   ```
   
   Or manually:
   ```bash
   pip install -r requirements.txt
   python find_keyboard.py
   ```

3. **The script will show your keyboard's USB IDs** - verify they match the defaults, or update them in `keyboard_controller.py` if different

## Running

Once setup is complete:

```bash
# Start the RGB sync
python main.py
```

Press `Ctrl+C` to stop.

## Troubleshooting

**Python not found?**
- Make sure you installed Python with "Add Python to PATH" checked
- Restart Command Prompt/PowerShell after installing

**Keyboard not found?**
- Run `python find_keyboard.py` to see all connected USB devices
- Check that your Rakk Ilis appears in the list
- Update `VENDOR_ID` and `PRODUCT_ID` in `keyboard_controller.py` if needed

**Colors aren't changing?**
- Close any official Rakk RGB software
- Unplug the keyboard, wait 3 seconds, plug it back in
- Run `python test.py` to diagnose

**Permission errors?**
- Windows shouldn't have these, but try running Command Prompt as Administrator

## Testing

Before running the main script, test everything:

```bash
python test.py
```

This will verify:
- ✓ Screen capture works
- ✓ Keyboard is found
- ✓ RGB commands work

## Full Documentation

See the main [README.md](README.md) for detailed information.
