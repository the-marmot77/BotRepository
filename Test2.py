from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

import pyautogui
import time


try: 
    img = pyautogui.locateOnScreen('Rapid.PNG', confidence=0.7)
    pyautogui.moveTo(img)
    print('success')
except pyautogui.ImageNotFoundException:
    print('Image not found')