from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Iterable

import pyautogui
from pyclick import HumanClicker

from utilities.geometry import Rectangle
from utilities.imagesearch import search_img_in_rect

pyautogui.FAILSAFE = True

hc = HumanClicker()
ASSETS = Path(__file__).resolve().parent / "BotImages"
IMAGE_PATHS = {
    "inventory": [
        ASSETS / "Inventory.png",
        ASSETS / "Inventory2.png",
    ],
    "prayers": [
        ASSETS / "Prayer_icon.png",
        ASSETS / "Prayer_icon2.png",
        ASSETS / "Prayer_icon3.png",
    ],
    "rapid": [
        ASSETS / "Rapid_Heal.png",
        ASSETS / "Rapid_Heal2.png",
    ],
    "potions": [
        ASSETS / "Super_combat_potion(4).png",
        ASSETS / "Super_combat_potion(3).png",
        ASSETS / "Super_combat_potion(2).png",
        ASSETS / "Super_combat_potion(1).png",
    ],
}

CLICK_INTERVAL_RANGE = (30.0, 36.0)
DURATION_LIMIT = 420
start_time = time.time()


def locate_and_click(
    image_path: Path, is_double_click: bool = False, confidence: float = 0.2
) -> bool:
    screen_rect = Rectangle(0, 0, pyautogui.size().width, pyautogui.size().height)
    found_rect = search_img_in_rect(str(image_path), screen_rect, confidence=confidence)

    if not found_rect:
        print(f"[nmz] Could not locate {image_path.name}")
        return False

    center_x, center_y = found_rect.get_center()
    hc.move((center_x, center_y), duration=random.uniform(1.1, 3.0))
    if is_double_click:
        pyautogui.doubleClick(interval=0.1)
    else:
        pyautogui.click()

    print(f"[nmz] Clicked {image_path.name} at ({center_x}, {center_y})")
    return True


def locate_and_click_any(
    image_paths: Iterable[Path], is_double_click: bool = False, confidence: float = 0.2
) -> bool:
    for path in image_paths:
        if locate_and_click(path, is_double_click=is_double_click, confidence=confidence):
            return True
    return False


def check_and_execute_reboost() -> bool:
    global start_time

    if time.time() - start_time <= DURATION_LIMIT:
        return False

    print("[nmz] 420 seconds passed. Triggering reboost.")

    if locate_and_click_any(IMAGE_PATHS["inventory"]):
        for potion in IMAGE_PATHS["potions"]:
            if locate_and_click(potion, confidence=0.7):
                start_time = time.time()
                break

        locate_and_click_any(IMAGE_PATHS["prayers"])
        print("[nmz] Reboost successful.")
    else:
        print("[nmz] Could not locate inventory.")
    return True


def run_actions() -> None:
    hc.move((100, 100), 2)
    consecutive_failures = 0

    while True:
        if check_and_execute_reboost():
            print("[nmz] Waiting 5 seconds before resuming...")
            time.sleep(5)
            continue

        if locate_and_click_any(IMAGE_PATHS["rapid"], is_double_click=True):
            sleep_time = random.uniform(*CLICK_INTERVAL_RANGE)
            print(f"[nmz] Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("[nmz] Rapid Heal not found three times. Exiting.")
                break
            print(f"[nmz] Rapid Heal not found (attempt {consecutive_failures}). Trying prayers...")
            locate_and_click_any(IMAGE_PATHS["prayers"])
            time.sleep(5)


if __name__ == "__main__":
    run_actions()
