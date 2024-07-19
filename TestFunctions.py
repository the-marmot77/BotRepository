import pyautogui, sys
import time


click = True

while click: 
    time.sleep(5)
    mouse = pyautogui.displayMousePosition()
    print(mouse)