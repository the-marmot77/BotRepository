import math
import random
import time
import pyautogui

pyautogui.FAILSAFE = True  # emergency stop via top-left corner


def ease_in_out(t: float) -> float:
    # Smooth start/stop on a straight line
    return 3 * t * t - 2 * t * t * t


def straightish_move_to(dest_xy, move_min: float, move_max: float, path_style: str):
    """
    Straight-biased mouse movement with optional mild/natural side wobble.
    path_style: "Straight" | "Mild" | "Natural"
    """
    start = pyautogui.position()
    sx, sy = start.x, start.y
    tx, ty = dest_xy
    dx, dy = tx - sx, ty - sy
    dist = math.hypot(dx, dy)
    if dist == 0:
        return

    dur = random.uniform(move_min, move_max)
    steps = max(12, min(120, int(dist / 8)))

    # Perpendicular unit vector
    nx, ny = (-dy / dist, dx / dist)

    if path_style == "Straight":
        amp = 0.0
    elif path_style == "Mild":
        amp = 0.02 * dist
    else:  # "Natural"
        amp = 0.06 * dist
    amp *= random.uniform(0.7, 1.1)

    per_step = dur / steps
    for i in range(1, steps + 1):
        t = i / steps
        e = ease_in_out(t)
        x = sx + dx * e
        y = sy + dy * e

        if amp > 0:
            wobble = math.sin(math.pi * e) * amp
            wobble *= random.uniform(0.85, 1.15)
            x += nx * wobble
            y += ny * wobble

        pyautogui.moveTo(x, y)
        time.sleep(per_step * random.uniform(0.9, 1.1))

    pyautogui.moveTo(tx, ty)
