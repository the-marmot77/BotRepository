# OPEN CV ALSO REQUIRED

from PIL import ImageGrab # Required install for this to run properly
from functools import partial
import pyautogui
import time
import random

# Configure ImageGrab to capture all screens
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Global variables for control and interval settings
click = True
duration_limit = 420  # Duration limit in seconds (7 minutes)
start_time = time.time()


def get_random_interval(min_val, max_val):
    """Generate a random interval between min_val and max_val."""
    return random.uniform(min_val, max_val)


def check_and_execute_reboost():
    """Check if the duration limit has passed and execute a reboost action."""
    global start_time  # Ensure we can reset the start time
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > duration_limit:
        print("420 seconds have passed. Reboosting.")
        mouse = pyautogui.position()
        inv = pyautogui.locateOnScreen("Images\Inventory.PNG", confidence=0.9)

        if inv:
            pyautogui.moveTo(inv, duration=0.5)
            pyautogui.click(inv)

            # List of potion images in the order of priority
            potions = [
                "Images\4dose.PNG",
                "Images\3dose.PNG",
                "Images\2dose.PNG",
                "Images\1dose.PNG",
            ]

            for potion in potions:
                try:
                    pot = pyautogui.locateOnScreen(potion, confidence=0.7)
                    if pot:
                        pyautogui.click(pot, duration=0.5)
                        print(f"Clicked on {potion}.")
                        # Reset the timer after a successful click
                        start_time = time.time()
                        break  # Exit the loop after clicking the first available potion
                except pyautogui.ImageNotFoundException:
                    print(f"Could not locate {potion}. Continuing to next potion.")
                    continue

            prayer = pyautogui.locateOnScreen("Images\Prayer.PNG", confidence=0.9)
            time.sleep(1)

            if prayer:
                pyautogui.click(prayer, duration=0.5)
                print("Clicked on Prayer tab.")
            else:
                print("Unable to locate prayer tab.")

            pyautogui.moveTo(mouse)
            print(f"Reboost successful.")
        else:
            print(f"Could not locate inventory.")
        return True
    return False


def click_rapid_icon():
    """Click the specified icon at random intervals between a and b."""
    global click  # Global click variable
    while click:
        if check_and_execute_reboost():
            print("Reboost Complete.")
            time.sleep(5)
            continue

        random_interval = get_random_interval(30.0, 36.0)
        mouse = pyautogui.position()

        try:
            # Attempt to locate the 'Rapid.PNG' icon
            icon = pyautogui.locateOnScreen("Images\Rapid.PNG", confidence=0.9)
            if not icon:
                # If 'Rapid.PNG' is not found, click on the 'Prayer.PNG' icon first
                prayer_icon = pyautogui.locateOnScreen(
                    "Images\Prayer.PNG", confidence=0.9
                )
                if prayer_icon:
                    pyautogui.click(prayer_icon)
                    # Reattempt to locate 'Rapid.PNG' after clicking 'Prayer.PNG'
                    icon = pyautogui.locateOnScreen("Images\Rapid.PNG", confidence=0.9)

            if icon:
                pyautogui.moveTo(icon)
                pyautogui.doubleClick(icon, interval=0.1)
                pyautogui.moveTo(mouse)
                print(f"Clicked on 'Rapid.PNG'.")
            else:
                print("Could not locate 'Rapid.PNG'.")

            print(f"Sleeping for: {random_interval:.2f} seconds")
            time.sleep(random_interval)

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    click_rapid_icon()
