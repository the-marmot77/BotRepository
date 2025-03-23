import time
import random
import numpy as np

from pyclick import HumanClicker
import pyautogui

from utilities.visualizesearch import visualize_search_area
from utilities.geometry import Rectangle
from utilities.imagesearch import search_img_in_rect

hc = HumanClicker()

CONFIDENCE_LEVELS = [0.15, 0.20, 0.25, 0.30]

IMAGE_PATHS = {
    "inventorys": [
        "PlankMake/BotImages/Inventory.png",
        "PlankMake/BotImages/Inventory2.png",
    ],
    "prayers": [
        "PlankMake/BotImages/Prayer_icon.png",
        "PlankMake/BotImages/Prayer_icon2.png",
        "PlankMake/BotImages/Prayer_icon3.png",
    ],
    "rapids": [
        "PlankMake/BotImages/Rapid_Heal.png",
        "PlankMake/BotImages/Rapid_Heal2.png",
    ],
    "potions": [
        "PlankMake/BotImages/Super_combat_potion(4).png",
        "PlankMake/BotImages/Super_combat_potion(3).png",
        "PlankMake/BotImages/Super_combat_potion(2).png",
        "PlankMake/BotImages/Super_combat_potion(1).png",
    ],
}

CLICK_INTERVAL_RANGE = (30.0, 36.0)
DURATION_LIMIT = 420  # Reboost timer in seconds
start_time = time.time()

def get_bottom_right_quadrant() -> Rectangle:
    width, height = pyautogui.size()
    return Rectangle(width // 2, height // 2, width // 2, height // 2)

def locate_and_click(image_path, is_double_click=False, confidence_levels=CONFIDENCE_LEVELS):
    screen_rect = get_bottom_right_quadrant()
    # visualize_search_area(screen_rect, duration=1)

    for confidence in confidence_levels:
        found_rect = search_img_in_rect(image_path, screen_rect, confidence=confidence)
        if found_rect:
            center_x, center_y = found_rect.get_center()
            hc.move((center_x, center_y), duration=random.uniform(1.1, 3.0))

            if is_double_click:
                pyautogui.doubleClick(interval=0.1)
            else:
                pyautogui.click()

            print(f"Clicked on {image_path} at ({center_x}, {center_y}) using confidence {confidence}")
            return True

    print(f"Could not locate {image_path} with any confidence level.")
    return False

def locate_and_click_any(image_paths, is_double_click=False, confidence_levels=CONFIDENCE_LEVELS):
    for path in image_paths:
        if locate_and_click(path, is_double_click=is_double_click, confidence_levels=confidence_levels):
            return True
    return False

def check_and_execute_reboost():
    global start_time

    if time.time() - start_time > DURATION_LIMIT:
        print("Reboosting after duration limit exceeded.")

        if locate_and_click_any(IMAGE_PATHS["inventorys"]):
            for potion in IMAGE_PATHS["potions"]:
                if locate_and_click(potion, confidence_levels=[0.6]):
                    start_time = time.time()
                    break

            locate_and_click_any(IMAGE_PATHS["prayers"])
            print("✅ Reboost successful.")
        else:
            print("❌ Could not locate inventory.")
        return True
    return False

def run_actions():
    time.sleep(5)
    hc.move((100, 100), 2)
    error_count = 0

    while True:
        if check_and_execute_reboost():
            print("Reboost Complete. Waiting 5 seconds...")
            time.sleep(5)
            continue

        if locate_and_click_any(IMAGE_PATHS["rapids"], is_double_click=True):
            sleep_time = random.uniform(*CLICK_INTERVAL_RANGE)
            print(f"Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        else:
            error_count += 1
            print(f"Attempt {error_count}: Rapid Heal not found.")
            if error_count >= 3:
                print("Too many failures. Exiting...")
                break
            locate_and_click_any(IMAGE_PATHS["prayers"])
            print("Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_actions()
