from PIL import ImageGrab
from functools import partial
import pyautogui
import time
import random

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

pyautogui.locateCenterOnScreen(pyautogui.pixelMatchesColor())



def find_color_position(color, tolerance=10):
    """Find the position of a given color on the screen."""
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")
    for x in range(0, width, 85):  # Step by 150 pixels horizontally
        for y in range(0, height, 85):  # Step by 150 pixels vertically
            current_color = pyautogui.pixel(x, y)
            if pyautogui.pixelMatchesColor(x, y, color, tolerance=tolerance):
                print(
                    f"Matching color found at ({x}, {y}) with current_color: {current_color}"
                )
                return (x, y)
            else:
                print(f"No match at ({x}, {y}) - Current color: {current_color}")
    return None