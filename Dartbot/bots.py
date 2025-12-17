import threading
import time
import random
import pyautogui
from .movement import straightish_move_to

pyautogui.FAILSAFE = True


class BaseBot:
    """Threaded loop with start/pause/exit and UI callbacks."""

    def __init__(self, name: str):
        self.name = name
        self.running = False
        self.exit_flag = False
        self._thread = threading.Thread(target=self._loop_wrapper, daemon=True)

        # shared settings
        self.pos1 = None
        self.pos2 = None
        self.min_delay = 0.9
        self.max_delay = 1.6
        self.move_min = 0.25
        self.move_max = 0.7
        self.jitter = 6
        self.path_style = "Mild"  # "Straight" | "Mild" | "Natural"

        # bolts-only
        self.fixed_wait = 2.0

        # UI hooks
        self.on_status = lambda s: None
        self.on_running_changed = lambda r: None

    # lifecycle
    def ensure_thread(self):
        if not self._thread.is_alive():
            self._thread = threading.Thread(target=self._loop_wrapper, daemon=True)
            self._thread.start()

    def start(self):
        self.ensure_thread()
        self.running = True
        self.on_running_changed(True)

    def pause(self):
        self.running = False
        self.on_running_changed(False)

    def toggle(self):
        self.ensure_thread()
        self.running = not self.running
        self.on_running_changed(self.running)
        return self.running

    def exit(self):
        self.running = False
        self.exit_flag = True

    # internals
    def _loop_wrapper(self):
        try:
            self.loop()
        except pyautogui.FailSafeException:
            self.running = False
            self.on_status("Stopped (failsafe)")
        except Exception as e:
            self.running = False
            self.on_status(f"Error: {e.__class__.__name__}")

    def loop(self):
        raise NotImplementedError

    # helpers
    def _jitter_point(self, base):
        return (
            base[0] + random.randint(-self.jitter, self.jitter),
            base[1] + random.randint(-self.jitter, self.jitter),
        )

    def _move_click(self, pt):
        straightish_move_to(pt, self.move_min, self.move_max, self.path_style)
        pyautogui.click(pt)

    def _sleep_rand(self):
        time.sleep(random.uniform(self.min_delay, self.max_delay))


class DartsBot(BaseBot):
    """click pos1 -> wait rand -> click pos2 -> wait rand -> repeat"""

    def __init__(self):
        super().__init__("Darts")

    def loop(self):
        self.on_status("Ready")
        while not self.exit_flag:
            if not self.running:
                time.sleep(0.05)
                continue
            if not (self.pos1 and self.pos2):
                self.on_status("Pick both positions")
                time.sleep(0.25)
                continue

            p1 = self._jitter_point(self.pos1)
            self._move_click(p1)
            self._sleep_rand()
            if not self.running:
                continue

            p2 = self._jitter_point(self.pos2)
            self._move_click(p2)
            self._sleep_rand()


class BoltsBot(BaseBot):
    """click pos1 -> click pos2 -> press space -> wait fixed -> repeat"""

    def __init__(self):
        super().__init__("Bolts")

    def loop(self):
        self.on_status("Ready")
        while not self.exit_flag:
            if not self.running:
                time.sleep(0.05)
                continue
            if not (self.pos1 and self.pos2):
                self.on_status("Pick both positions")
                time.sleep(0.25)
                continue

            p1 = self._jitter_point(self.pos1)
            self._move_click(p1)

            p2 = self._jitter_point(self.pos2)
            self._move_click(p2)

            pyautogui.press("space")
            time.sleep(max(0.0, float(self.fixed_wait)))
