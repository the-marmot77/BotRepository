import threading
import time
import random
import pyautogui
from pyclick import HumanClicker

purple_color = (144, 0, 173)
hc = HumanClicker()
running = False  

def find_color_position(color, tolerance=10, step=250):
    """Find the position of a given color on the screen."""
    width, height = pyautogui.size()
    for x in range(0, width, step):
        for y in range(0, height, step):
            if pyautogui.pixelMatchesColor(x, y, color, tolerance=tolerance):
                return (x, y)
    return None

def click_color(color):
    """Finds and clicks the purple color on screen."""
    pos = find_color_position(color, tolerance=10)
    if pos:
        offset_x, offset_y = random.randint(-10, 10), random.randint(-10, 10)
        new_pos = (pos[0] + offset_x, pos[1] + offset_y)

        hc.move(new_pos, duration=random.uniform(0.8, 2.0))
        pyautogui.click(new_pos)
        print(f"Clicked on color {color} at {new_pos}")
        time.sleep(random.uniform(0.5, 1.5))
    else:
        print(f"Could not find color {color} on screen.")

def click_image(image_path):
    for _ in range(3):
        icon = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if icon:
            hc.move(icon, duration=random.uniform(0.8, 2.0))
            pyautogui.click(icon)
            print(f"Clicked on {image_path} at position {icon}.")
            time.sleep(random.uniform(0.5, 1.5))
            return
        time.sleep(0.5)
    print(f"Failed to locate {image_path} after 3 attempts.")

def click_colors_and_image_in_order():
    click_color(purple_color)
    click_image("PlankMake\MahogPlank.png")
    click_image("PlankMake\MahogLog.png")
    click_image("PlankMake\XButton2.PNG")
    pyautogui.press("f4")
    time.sleep(random.uniform(0.1, 0.5))
    click_image("PlankMake\Spell1.PNG")
    click_image("PlankMake\MahogLog.PNG")
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.press("f1")

def run_bot(iterations, min_delay, max_delay):
    global running
    running = True
    for i in range(iterations):
        if not running:
            print("Bot Stopped")
            return
        print(f"Iteration {i+1}")
        click_colors_and_image_in_order()
        time.sleep(random.uniform(min_delay, max_delay))
    print("Completed all iterations.")

def stop_bot():
    global running
    running = False

if __name__ == "__main__":
    run_bot(10, 95, 105)
