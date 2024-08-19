from PIL import ImageGrab
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

            # List of potion images in the order of priority
        images = ["Purple.PNG", "Logs.PNG", "White.PNG"]

        for img in images:
            try:
                clicks = pyautogui.locateOnScreen(img, confidence=0.7)
                if clicks:
                    pyautogui.click(clicks, duration=0.5)
                    print(f"Clicked on {img}.")
                    # Reset the timer after a successful click
                    start_time = time.time()
                    break  # Exit the loop after clicking the first available potion
            except pyautogui.ImageNotFoundException:
                print(f"Could not locate {img}. Continuing to next potion.")
                continue

        prayer = pyautogui.locateOnScreen("Prayer.PNG", confidence=0.7)
        time.sleep(1)

        if prayer:
            pyautogui.click(prayer, duration=0.5)
            print("Clicked on Prayer tab.")
        else:
            print("Unable to locate prayer tab.")

        pyautogui.moveTo(mouse)
        print(f"Reboost successful.")
        return True
    return False


def click_rapid_icon():
    """Click the specified icon at random intervals between a and b."""
    global click  # Ensure we use the global click variable
    while click:
        if check_and_execute_reboost():
            print("Reboost Complete.")
            time.sleep(5)
            continue

        random_interval = get_random_interval(30.0, 36.0)
        mouse = pyautogui.position()
        icon = pyautogui.locateOnScreen("Rapid.PNG", confidence=0.9)

        if icon:
            pyautogui.moveTo(icon)
            pyautogui.doubleClick(icon, interval=0.1)
            pyautogui.moveTo(mouse)
            print(f"Clicked on 'Rapid.PNG'.")
        else:
            print(f"Could not locate 'Rapid.PNG'.")

        print(f"Sleeping for: {random_interval:.2f} seconds")
        time.sleep(random_interval)


if __name__ == "__main__":
    click_rapid_icon()
