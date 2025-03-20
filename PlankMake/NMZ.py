from PIL import ImageGrab
from functools import partial
import pyautogui
import time
import random
from pyclick import HumanClicker

# Configure ImageGrab to capture all screens
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Global Variables
click = True
duration_limit = 420  # 7-minute limit
start_time = time.time()
hc = HumanClicker()

# Image Paths
IMAGE_PATHS = {
    "inventory": "PlankMake\BotImages\Inventory.png",
    "prayer": "PlankMake\BotImages\Prayer_icon.png",
    "rapid": "PlankMake\BotImages\Rapid_Heal.png",
    "potions": [
        "PlankMake\BotImages\Super_combat_potion(4).png",
        "PlankMake\BotImages\Super_combat_potion(3).png",
        "PlankMake\BotImages\Super_combat_potion(2).png",
        "PlankMake\BotImages\Super_combat_potion(1).png",
    ],
}


def get_random_interval(min_val, max_val):
    """Generate a random interval between min_val and max_val."""
    return random.uniform(min_val, max_val)


def locate_and_click(image_path, confidence=0.9, is_double_click=False):
    """Locate an image on the screen and click it."""
    if pos := pyautogui.locateCenterOnScreen(image_path, confidence=confidence):
        hc.move(pos, duration=get_random_interval(0.8, 2.0))
        if is_double_click:
            pyautogui.doubleClick(pos, interval=0.1)  # Only double click if specified
        else:
            pyautogui.click(pos)
        print(f"Clicked on {image_path}.")
        time.sleep(get_random_interval(0.5, 1.5))
        return True
    return False


def check_and_execute_reboost():
    """Check if the duration limit has passed and execute a reboost action."""
    global start_time

    if time.time() - start_time > duration_limit:
        print("420 seconds have passed. Reboosting.")

        if locate_and_click(IMAGE_PATHS["inventory"]):
            for potion in IMAGE_PATHS["potions"]:
                if locate_and_click(potion, confidence=0.7):
                    start_time = time.time()  # Reset timer after drinking a potion
                    break  # Stop after finding the highest dose

            locate_and_click(IMAGE_PATHS["prayer"])  # Open prayer tab after drinking potion
            print("Reboost successful.")
        else:
            print("Could not locate inventory.")
        return True
    return False


def click_rapid_icon():
    """Click the 'Rapid.PNG' icon at random intervals, ensuring it's double-clicked."""
    global click

    while click:
        if check_and_execute_reboost():
            print("Reboost Complete.")
            time.sleep(5)
            continue

        random_interval = get_random_interval(30.0, 36.0)

        # Double-click Rapid Heal (if found); otherwise, open Prayer tab and retry
        if not locate_and_click(IMAGE_PATHS["rapid"], is_double_click=True):
            print("Could not locate 'Rapid.PNG'. Checking for Prayer tab.")
            if locate_and_click(IMAGE_PATHS["prayer"]):  # Open Prayer tab if Rapid isn't visible
                locate_and_click(IMAGE_PATHS["rapid"], is_double_click=True)

        print(f"Sleeping for: {random_interval:.2f} seconds")
        time.sleep(random_interval)


if __name__ == "__main__":
    click_rapid_icon()
