import time
import random
import numpy as np

from pyclick import HumanClicker
import pyautogui

from utilities.geometry import Rectangle
from utilities.imagesearch import search_img_in_rect

hc = HumanClicker()

# Paths to all images
IMAGE_PATHS = {
    "inventory": "PlankMake/BotImages/Inventory.png",
    "prayers": [
        "PlankMake/BotImages/Prayer_icon.png",
        "PlankMake/BotImages/Prayer_icon2.png"
    ],
    "rapid": "PlankMake/BotImages/Rapid_Heal.png",
    "potions": [
        "PlankMake/BotImages/Super_combat_potion(4).png",
        "PlankMake/BotImages/Super_combat_potion(3).png",
        "PlankMake/BotImages/Super_combat_potion(2).png",
        "PlankMake/BotImages/Super_combat_potion(1).png",
    ],
}

CLICK_INTERVAL_RANGE = (30.0, 36.0)
DURATION_LIMIT = 420
start_time = time.time()

def capture_screen():
    screenshot = pyautogui.screenshot()
    return np.array(screenshot)

def locate_and_click(image_path, is_double_click=False, confidence=0.15):
    screen_rect = Rectangle(0, 0, pyautogui.size().width, pyautogui.size().height)
    found_rect = search_img_in_rect(image_path, screen_rect, confidence=confidence)

    if found_rect:
        center_x, center_y = found_rect.get_center()
        hc.move((center_x, center_y), duration=random.uniform(1.1, 3.0))

        if is_double_click:
            pyautogui.doubleClick(interval=0.1)
        else:
            pyautogui.click()

        print(f"✅ Clicked on {image_path} at ({center_x}, {center_y})")
        return True
    else:
        print(f"❌ Could not locate {image_path}.")
        return False

def locate_and_click_any(image_paths, is_double_click=False, confidence=0.15):
    for path in image_paths:
        if locate_and_click(path, is_double_click=is_double_click, confidence=confidence):
            return True
    return False

def check_and_execute_reboost():
    global start_time

    if time.time() - start_time > DURATION_LIMIT:
        print("420 seconds have passed. Reboosting.")

        if locate_and_click(IMAGE_PATHS["inventory"]):
            for potion in IMAGE_PATHS["potions"]:
                if locate_and_click(potion, confidence=0.7):
                    start_time = time.time()
                    break

            locate_and_click_any(IMAGE_PATHS["prayers"])
            print("✅ Reboost successful.")
        else:
            print("❌ Could not locate inventory.")
        return True
    return False

def run_actions():
    hc.move((100, 100), 2)
    e = 0

    while True:
        if check_and_execute_reboost():
            print("Reboost Complete. Waiting 5 seconds before continuing...")
            time.sleep(5)
            continue

        if locate_and_click(IMAGE_PATHS["rapid"], is_double_click=True):
            sleep_time = random.uniform(*CLICK_INTERVAL_RANGE)
            print(f"Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        else:
            if e >= 3:
                break
            e += 1
            print("Attempt", e)
            print("Rapid heal not found, switching to prayer tab...")
            locate_and_click_any(IMAGE_PATHS["prayers"], is_double_click=False)
            print("Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_actions()
