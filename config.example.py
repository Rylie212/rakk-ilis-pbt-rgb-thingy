"""
Configuration file for Rakk Ilis RGB Sync
Copy this to config.py and modify settings as needed
"""

# USB Device Configuration
USB_CONFIG = {
    'vendor_id': 0x3151,      # Rakk vendor ID
    'product_id': 0x4154,     # Rakk Ilis product ID (update if different)
}

# Screen Capture Configuration
SCREEN_CONFIG = {
    'mode': 'full_screen',    # Options: 'full_screen', 'region'
    'region': {
        'x': 0,
        'y': 0,
        'width': 1920,
        'height': 1080,
    },
    'sample_rate': 60,        # Hz (frames per second)
}

# Color Update Configuration
COLOR_CONFIG = {
    'min_distance': 5,        # Minimum color distance to trigger update (0-255)
    'smoothing_steps': 30,    # Steps for smooth color transitions (0 = instant)
    'smoothing_enabled': False,
}

# RGB Lighting Configuration
RGB_CONFIG = {
    'brightness': 255,        # 0-255
    'mode': 'static',         # Options: 'static', 'breathing', 'rainbow'
}

# Debug Configuration
DEBUG_CONFIG = {
    'verbose': False,         # Print more debug information
    'show_fps': False,        # Show sampling FPS
    'log_colors': False,      # Log every color change
}
