import time
import numpy as np
import pyautogui
from pyclick import HumanClicker
from utilities.geometry import Rectangle
import random as r

hc = HumanClicker()

def get_top_half_screen() -> Rectangle:
    width, height = pyautogui.size()
    return Rectangle(0, 0, width, height // 2)

def generate_saccade_points(area: Rectangle, step: int = 50) -> list[tuple[int, int]]:
    """
    Generates points across the screen in a randomized saccade-like order.
    """
    points = []
    for y in range(area.top, area.top + area.height, step):
        for x in range(area.left, area.left + area.width, step):
            points.append((x, y))
    r.shuffle(points)
    return points

def find_color_saccade(target_color: tuple, area: Rectangle, step: int = 50, tolerance: int = 10) -> tuple | None:
    screenshot = area.screenshot()
    points = generate_saccade_points(area, step)

    for x, y in points:
        if y >= screenshot.shape[0] or x >= screenshot.shape[1]:
            continue
        pixel = screenshot[y, x]
        if np.all(np.abs(pixel.astype(int) - np.array(target_color)) <= tolerance):
            return (x + area.left, y + area.top)

    return None

def run_color_bot():
    target_color = (255, 0, 202)  # Magenta-ish color
    area = get_top_half_screen()

    while True:
        pos = find_color_saccade(target_color, area, step=50)
        if pos:
            print(f"🎯 Found target color at: {pos}")
            hc.move(pos, duration=r.uniform(0.8, 1.0))
            pyautogui.click()
        else:
            print("❌ Target color not found.")
        time.sleep(r.uniform(2.4, 4.0))

if __name__ == "__main__":
    run_color_bot()
