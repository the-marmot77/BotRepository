from __future__ import annotations

import random as r
import time
from pathlib import Path

import numpy as np
import pyautogui
from pyclick import HumanClicker

from utilities.geometry import Rectangle
from utilities.imagesearch import search_img_in_rect

pyautogui.FAILSAFE = True

hc = HumanClicker()
ASSETS = Path(__file__).resolve().parent / "BotImages"
IMAGE_PATHS = {
    "knife": ASSETS / "Knife.png",
    "bluegill": ASSETS / "Bluegill.png",
}


def get_top_half_screen() -> Rectangle:
    width, height = pyautogui.size()
    return Rectangle(0, 0, width, height // 2)


def get_lower_right_quarter() -> Rectangle:
    width, height = pyautogui.size()
    return Rectangle(width // 2, height // 2, width // 2, height // 2)


def generate_saccade_points(area: Rectangle, step: int = 50) -> list[tuple[int, int]]:
    """Generates points across the screen in a randomized saccade-like order."""
    points = []
    for y in range(area.top, area.top + area.height, step):
        for x in range(area.left, area.left + area.width, step):
            points.append((x, y))
    r.shuffle(points)
    return points


def find_color_saccade(
    target_color: tuple[int, int, int],
    area: Rectangle,
    step: int = 50,
    tolerance: int = 10,
) -> tuple[int, int] | None:
    screenshot = area.screenshot()
    points = generate_saccade_points(area, step)

    for x, y in points:
        if y >= screenshot.shape[0] or x >= screenshot.shape[1]:
            continue
        pixel = screenshot[y, x]
        if np.all(np.abs(pixel.astype(int) - np.array(target_color)) <= tolerance):
            return (x + area.left, y + area.top)

    return None


def run_color_bot() -> None:
    target_color = (255, 0, 202)
    area1 = get_top_half_screen()
    area2 = get_lower_right_quarter()

    i = 0
    while True:
        if i >= 24:
            knife = search_img_in_rect(str(IMAGE_PATHS["knife"]), area2, confidence=0.15)
            fish = search_img_in_rect(str(IMAGE_PATHS["bluegill"]), area2, confidence=0.15)

            if knife and fish:
                hc.move(knife.get_center(), duration=r.uniform(0.8, 1.0))
                hc.click()
                time.sleep(r.uniform(1.4, 2.0))
                hc.move(fish.get_center(), duration=r.uniform(0.4, 0.8))
                hc.click()
                print("[aerial] Used knife on fish")
            else:
                print("[aerial] Knife or fish not found in action bar")

            time.sleep(r.uniform(45.0, 55.0))
            i = 0
            continue

        pos = find_color_saccade(target_color, area1, step=35)
        if pos:
            print(f"[aerial] Found target color at {pos}")
            hc.move(pos, duration=r.uniform(0.8, 1.0))
            pyautogui.click()
            i += 1
            print("[aerial] Iteration:", i)
        else:
            print("[aerial] Target color not found.")

        time.sleep(r.uniform(2.4, 4.0))


if __name__ == "__main__":
    run_color_bot()
