"""Screen color sampling module for RGB sync."""

import mss
from PIL import Image
import numpy as np


class ScreenCapture:
    """Captures and analyzes screen color for RGB sync."""

    def __init__(self):
        """Initialize the screen capture tool."""
        self.sct = mss.mss()

    def get_average_screen_color(self):
        """
        Capture the entire screen and return the average RGB color.
        
        Returns:
            tuple: (R, G, B) values from 0-255
        """
        # Capture the primary monitor
        monitor = self.sct.monitors[1]  # 1 is the primary monitor
        screenshot = self.sct.grab(monitor)

        # Convert to PIL Image and then to numpy array for faster processing
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Calculate average color across all pixels
        avg_color = np.mean(img_array, axis=(0, 1))
        
        # Convert to 0-255 integers
        r, g, b = [int(c) for c in avg_color]
        
        return (r, g, b)

    def get_region_color(self, x, y, width, height):
        """
        Capture a specific region and return its average color.
        
        Args:
            x, y: Top-left coordinates
            width, height: Region dimensions
            
        Returns:
            tuple: (R, G, B) values from 0-255
        """
        region = {
            'top': y,
            'left': x,
            'width': width,
            'height': height
        }
        
        screenshot = self.sct.grab(region)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        img_array = np.array(img)
        
        avg_color = np.mean(img_array, axis=(0, 1))
        r, g, b = [int(c) for c in avg_color]
        
        return (r, g, b)

    def close(self):
        """Clean up resources."""
        pass
