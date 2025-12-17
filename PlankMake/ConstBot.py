from __future__ import annotations

import random
import time
from functools import partial
from pathlib import Path

import pyautogui
from PIL import ImageGrab

# Configure ImageGrab to capture all screens
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
pyautogui.FAILSAFE = True

# Define RGB values for the butler and the bench colors
butler_color = (144, 0, 173)  # Butler: FF9000AD -> (144, 0, 173)
bench_color = (255, 231, 0)  # Bench: FFFFFE700 -> (255, 231, 0)
ASSETS = Path(__file__).resolve().parent / "BotImages"


def find_color_position(color, tolerance=10):
    """Find the position of a given color on the screen."""
    width, height = pyautogui.size()
    for x in range(0, width, 115):  # Step by 150 pixels horizontally
        for y in range(0, height, 115):  # Step by 150 pixels vertically
            current_color = pyautogui.pixel(x, y)
            if pyautogui.pixelMatchesColor(x, y, color, tolerance=tolerance):
                print(f"Matching color found at ({x}, {y})")
                return (x, y)
    return None


def click_color(color, tolerance=10):
    """Find and click the given color on the screen with random offset."""
    pos = find_color_position(color, tolerance)
    if pos:
        offset_x = random.randint(10, 20)
        offset_y = random.randint(10, 20)
        new_pos = (pos[0] + offset_x, pos[1] + offset_y)

        pyautogui.moveTo(new_pos, duration=random.uniform(0.3, 1.0))
        pyautogui.click(new_pos)
        print(
            f"Clicked on color at position {new_pos} with offsets ({offset_x}, {offset_y})."
        )
        time.sleep(random.uniform(0.5, 1.5))
    else:
        print(f"Could not locate the color {color} on the screen.")


def send_butler_to_bank():
    """Click on the butler and instruct them to fetch exactly 24 planks."""
    print("Looking for the butler...")
    click_color(butler_color)
    pyautogui.press(
        "1"
    )  # Assuming pressing '1' instructs the butler to fetch 24 planks
    time.sleep(1)  # Wait for butler to fetch planks and return


def build_teak_bench():
    """Find the bench space, click, and press '1' to build the teak bench."""
    print("Looking for bench space...")
    click_color(bench_color)  # Click on the bench space
    pyautogui.press("2")  # Press '1' to confirm building
    time.sleep(3)  # Wait for the bench to be built


def remove_teak_bench():
    """Find the built bench, click, and press '1' to remove the bench."""
    print("Looking for built bench...")
    click_color(bench_color)  # Click on the built bench
    pyautogui.press("1")  # Press '1' to confirm removal
    time.sleep(2)  # Wait for the bench to be removed


def check_for_butler_payment():
    """Check if the Butler is asking for payment and pay him."""
    payment_prompt = pyautogui.locateOnScreen(str(ASSETS / "ButlerPayment.png"), confidence=0.9)
    if payment_prompt:
        pyautogui.press("space")
        time.sleep(0.5)
        pyautogui.press("1")
        time.sleep(0.5)
        pyautogui.press("space")
        time.sleep(2)


def automate_construction():
    """Automate the entire building and removing process."""
    for i in range(10):  # Adjust the number of repetitions as needed
        print(f"Iteration {i + 1}")

        # Build and remove 4 benches (using 24 planks)
        for _ in range(4):
            build_teak_bench()  # Build the bench
            remove_teak_bench()  # Remove the bench

        send_butler_to_bank()  # Send butler to fetch 24 planks after 4 benches
        time.sleep(random.uniform(10, 15))  # Random delay between loops

        # Check for payment prompt after each bank fetch
        check_for_butler_payment()


if __name__ == "__main__":
    print("Starting in 5 seconds...")
    time.sleep(5)  # Allow time to switch to the game window
    automate_construction()
    print("Completed all iterations.")
