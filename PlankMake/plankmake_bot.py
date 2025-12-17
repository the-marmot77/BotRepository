from __future__ import annotations

import random
import threading
import time
from pathlib import Path
from typing import Optional, Tuple

import pyautogui
from pyclick import HumanClicker

pyautogui.FAILSAFE = True

ASSETS_DIR = Path(__file__).resolve().parent / "BotImages"


class PlankMakeBot:
    """Automates converting mahogany logs into planks using image matching."""

    def __init__(self, step: int = 200) -> None:
        self._running = threading.Event()
        self._scan_step = step
        self._target_color = (144, 0, 173)
        self._hc = HumanClicker()

    # -------- public API --------
    def run(self, iterations: int, min_delay: float, max_delay: float) -> None:
        """Runs the plank-making loop until the requested iterations or stop()."""
        self._running.set()
        lo, hi = sorted((min_delay, max_delay))
        for idx in range(1, iterations + 1):
            if not self._running.is_set():
                print("[plankmake] Stopped by user")
                return
            print(f"[plankmake] Iteration {idx}/{iterations}")
            self._click_sequence()
            sleep_for = random.uniform(lo, hi)
            time.sleep(sleep_for)
        print("[plankmake] Completed all iterations")

    def stop(self) -> None:
        self._running.clear()

    # -------- sequence helpers --------
    def _click_sequence(self) -> None:
        self._click_target_color()
        self._click_asset("MahogPlank.png")
        self._click_asset("MahogLog.png")
        self._click_asset("XButton2.PNG")
        pyautogui.press("f4")
        time.sleep(random.uniform(0.1, 0.5))
        self._click_asset("Spell1.PNG")
        self._click_asset("MahogLog.PNG")
        time.sleep(random.uniform(0.1, 0.5))
        pyautogui.press("f1")

    def _click_target_color(self) -> None:
        location = self._find_color_position(self._target_color)
        if not location:
            print("[plankmake] Target color not found on screen")
            return

        jittered = (
            location[0] + random.randint(-10, 10),
            location[1] + random.randint(-10, 10),
        )
        self._hc.move(jittered, duration=random.uniform(0.8, 2.0))
        pyautogui.click(jittered)
        print(f"[plankmake] Clicked target color at {jittered}")
        time.sleep(random.uniform(0.5, 1.5))

    def _click_asset(self, filename: str, retries: int = 3) -> None:
        asset_path = str(ASSETS_DIR / filename)
        for attempt in range(1, retries + 1):
            location = pyautogui.locateCenterOnScreen(asset_path, confidence=0.8)
            if location:
                self._hc.move(location, duration=random.uniform(0.6, 1.2))
                pyautogui.click(location)
                print(f"[plankmake] Clicked {filename} at {location}")
                time.sleep(random.uniform(0.5, 1.5))
                return
            time.sleep(0.5)
            print(f"[plankmake] {filename} not found (attempt {attempt}/{retries})")

    # -------- low-level utilities --------
    def _find_color_position(
        self, color: Tuple[int, int, int], tolerance: int = 10
    ) -> Optional[Tuple[int, int]]:
        width, height = pyautogui.size()
        for x in range(0, width, self._scan_step):
            for y in range(0, height, self._scan_step):
                if pyautogui.pixelMatchesColor(x, y, color, tolerance=tolerance):
                    return (x, y)
        return None


_BOT = PlankMakeBot()


def run_bot(iterations: int, min_delay: float, max_delay: float) -> None:
    _BOT.run(iterations, min_delay, max_delay)


def stop_bot() -> None:
    _BOT.stop()


if __name__ == "__main__":
    run_bot(iterations=10, min_delay=95, max_delay=105)
