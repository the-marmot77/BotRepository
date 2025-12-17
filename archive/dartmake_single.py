# dartmake_single.py
import threading
import time
import random
import math
import tkinter as tk
from tkinter import ttk, messagebox

import pyautogui
from pynput import keyboard

# Optional dark theme. Falls back to Tkinter if missing.
try:
    import ttkbootstrap as tb
    HAS_BOOTSTRAP = True
except Exception:
    HAS_BOOTSTRAP = False

# PyAutoGUI safety and speed
pyautogui.FAILSAFE = True            # Move mouse to top-left for emergency stop
pyautogui.PAUSE = 0                  # No built-in pause between actions

# ---------------- Movement ----------------
def ease_in_out(t: float) -> float:
    return 3 * t * t - 2 * t * t * t

def move_fast_linear(dest_xy, move_min: float, move_max: float):
    """Single OS-level move. Fast and smooth."""
    dur = random.uniform(move_min, move_max)
    pyautogui.moveTo(dest_xy[0], dest_xy[1], duration=dur)

def move_smooth_straightish(dest_xy, move_min: float, move_max: float, path_style: str):
    """Straight-biased path with optional mild/natural wobble."""
    start = pyautogui.position()
    sx, sy = start.x, start.y
    tx, ty = dest_xy
    dx, dy = tx - sx, ty - sy
    dist = math.hypot(dx, dy)
    if dist <= 0:
        return

    dur = random.uniform(move_min, move_max)
    # Fewer steps for speed while keeping shape
    steps = max(10, min(60, int(dist / 18)))

    # Perpendicular unit vector
    nx, ny = (-dy / dist, dx / dist)

    # Amplitude by style
    if path_style == "Straight":
        amp = 0.0
    elif path_style == "Mild":
        amp = 0.02 * dist
    else:
        amp = 0.06 * dist
    amp *= random.uniform(0.85, 1.15)

    per_step = dur / steps
    for i in range(1, steps + 1):
        t = i / steps
        e = ease_in_out(t)
        x = sx + dx * e
        y = sy + dy * e
        if amp > 0:
            wobble = math.sin(math.pi * e) * amp
            x += nx * wobble
            y += ny * wobble
        pyautogui.moveTo(x, y)
        # Small sleep. Keep it tight to reduce lag.
        time.sleep(per_step)

    pyautogui.moveTo(tx, ty)

def move_cursor(dest_xy, engine: str, move_min: float, move_max: float, path_style: str):
    if engine == "Fast":
        move_fast_linear(dest_xy, move_min, move_max)
    else:
        move_smooth_straightish(dest_xy, move_min, move_max, path_style)

# ---------------- Bots ----------------
class BaseBot:
    def __init__(self, name: str):
        self.name = name
        self.running = False
        self.exit_flag = False
        self._thread = threading.Thread(target=self._loop_wrapper, daemon=True)

        # Shared settings
        self.pos1 = None
        self.pos2 = None
        self.min_delay = 0.9
        self.max_delay = 1.6
        self.move_min = 0.20
        self.move_max = 0.55
        self.jitter   = 5
        self.path_style = "Mild"       # Straight | Mild | Natural
        self.engine     = "Fast"       # Fast | Smooth

        # Bolts-only
        self.fixed_wait = 2.0

        # UI hooks
        self.on_status = lambda s: None
        self.on_running_changed = lambda r: None

    # Lifecycle
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

    # Internals
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

    # Helpers
    def _jitter_point(self, base):
        return (base[0] + random.randint(-self.jitter, self.jitter),
                base[1] + random.randint(-self.jitter, self.jitter))

    def _move_click(self, pt):
        move_cursor(pt, self.engine, self.move_min, self.move_max, self.path_style)
        pyautogui.click(pt)

    def _sleep_rand(self):
        time.sleep(random.uniform(self.min_delay, self.max_delay))


class DartsBot(BaseBot):
    def __init__(self):
        super().__init__("Darts")

    def loop(self):
        self.on_status("Ready")
        while not self.exit_flag:
            if not self.running:
                time.sleep(0.03)
                continue
            if not (self.pos1 and self.pos2):
                self.on_status("Pick both positions")
                time.sleep(0.2)
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
    def __init__(self):
        super().__init__("Bolts")

    def loop(self):
        self.on_status("Ready")
        while not self.exit_flag:
            if not self.running:
                time.sleep(0.03)
                continue
            if not (self.pos1 and self.pos2):
                self.on_status("Pick both positions")
                time.sleep(0.2)
                continue

            p1 = self._jitter_point(self.pos1)
            self._move_click(p1)

            p2 = self._jitter_point(self.pos2)
            self._move_click(p2)

            time.sleep(random.uniform(1.0, 2.0))
            pyautogui.press("space")
            time.sleep(float(self.fixed_wait) + random.uniform(-0.5, 0.5))

# ---------------- UI ----------------
class App:
    def __init__(self):
        self.root = tb.Window(themename="cyborg") if HAS_BOOTSTRAP else tk.Tk()
        self.root.title("dartmake")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.darts = DartsBot()
        self.bolts = BoltsBot()
        self.bots = [self.darts, self.bolts]

        self.darts.on_status = lambda s: self._set_status(0, s)
        self.bolts.on_status = lambda s: self._set_status(1, s)
        self.darts.on_running_changed = lambda r: self._set_running_ui(0, r)
        self.bolts.on_running_changed = lambda r: self._set_running_ui(1, r)

        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.tabs = ttk.Notebook(main)
        self.tabs.grid(row=0, column=0, sticky="nsew")

        self._build_darts_tab()
        self._build_bolts_tab()

        # Ensure threads exist
        for b in self.bots:
            b.ensure_thread()

        # Hotkeys
        threading.Thread(target=self._listen_hotkeys, daemon=True).start()

    # Darts tab
    def _build_darts_tab(self):
        f = ttk.Frame(self.tabs)
        self.tabs.add(f, text="Darts")

        # Targets
        lf_t = ttk.LabelFrame(f, text="Targets")
        lf_t.grid(row=0, column=0, sticky="ew", pady=(0,8))
        for c in range(4): lf_t.columnconfigure(c, weight=1)

        ttk.Label(lf_t, text="Position 1").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.d_pos1 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.d_pos1).grid(row=0, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(0, 1)).grid(row=0, column=2, padx=8)

        ttk.Label(lf_t, text="Position 2").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.d_pos2 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.d_pos2).grid(row=1, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(0, 2)).grid(row=1, column=2, padx=8)

        # Timing & Movement
        lf_tm = ttk.LabelFrame(f, text="Timing & Movement")
        lf_tm.grid(row=1, column=0, sticky="ew", pady=(0,8))
        for c in range(6): lf_tm.columnconfigure(c, weight=1)

        ttk.Label(lf_tm, text="Delay min (s)").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.d_min_delay = tk.DoubleVar(value=self.darts.min_delay)
        ttk.Spinbox(lf_tm, from_=0.0, to=999.0, increment=0.1, textvariable=self.d_min_delay, width=8)\
            .grid(row=0, column=1, sticky="w")

        ttk.Label(lf_tm, text="Delay max (s)").grid(row=0, column=2, sticky="w", padx=8, pady=6)
        self.d_max_delay = tk.DoubleVar(value=self.darts.max_delay)
        ttk.Spinbox(lf_tm, from_=0.0, to=999.0, increment=0.1, textvariable=self.d_max_delay, width=8)\
            .grid(row=0, column=3, sticky="w")

        ttk.Label(lf_tm, text="Move min (s)").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.d_move_min = tk.DoubleVar(value=self.darts.move_min)
        ttk.Spinbox(lf_tm, from_=0.0, to=5.0, increment=0.05, textvariable=self.d_move_min, width=8)\
            .grid(row=1, column=1, sticky="w")

        ttk.Label(lf_tm, text="Move max (s)").grid(row=1, column=2, sticky="w", padx=8, pady=6)
        self.d_move_max = tk.DoubleVar(value=self.darts.move_max)
        ttk.Spinbox(lf_tm, from_=0.0, to=5.0, increment=0.05, textvariable=self.d_move_max, width=8)\
            .grid(row=1, column=3, sticky="w")

        ttk.Label(lf_tm, text="Jitter ± px").grid(row=2, column=0, sticky="w", padx=8, pady=(6,8))
        self.d_jitter = tk.IntVar(value=self.darts.jitter)
        ttk.Spinbox(lf_tm, from_=0, to=100, increment=1, textvariable=self.d_jitter, width=8)\
            .grid(row=2, column=1, sticky="w")

        ttk.Label(lf_tm, text="Path style").grid(row=2, column=2, sticky="w", padx=8, pady=(6,8))
        self.d_path_style = tk.StringVar(value=self.darts.path_style)
        ttk.Combobox(lf_tm, textvariable=self.d_path_style, values=["Straight","Mild","Natural"],
                     width=10, state="readonly").grid(row=2, column=3, sticky="w")

        ttk.Label(lf_tm, text="Engine").grid(row=0, column=4, sticky="w", padx=8, pady=6)
        self.d_engine = tk.StringVar(value=self.darts.engine)
        ttk.Combobox(lf_tm, textvariable=self.d_engine, values=["Fast","Smooth"], width=10, state="readonly")\
            .grid(row=0, column=5, sticky="w")

        # Controls + Status
        ctl = ttk.Frame(f)
        ctl.grid(row=2, column=0, sticky="ew", pady=(0,8))
        ctl.columnconfigure(0, weight=1)
        ctl.columnconfigure(1, weight=1)
        ttk.Button(ctl, text="Start", command=lambda: self._start_tab(0)).grid(row=0, column=0, sticky="ew", padx=(0,4))
        ttk.Button(ctl, text="Stop",  command=lambda: self._stop_tab(0)).grid(row=0, column=1, sticky="ew", padx=(4,0))

        self.d_status = tk.StringVar(value="Idle  |  F8 = Start/Pause   Esc = Exit")
        ttk.Label(f, textvariable=self.d_status).grid(row=3, column=0, sticky="w")
        ttk.Label(f, text="Emergency stop: move mouse to top-left corner").grid(row=4, column=0, sticky="w")

    # Bolts tab
    def _build_bolts_tab(self):
        f = ttk.Frame(self.tabs)
        self.tabs.add(f, text="Bolts")

        lf_t = ttk.LabelFrame(f, text="Targets")
        lf_t.grid(row=0, column=0, sticky="ew", pady=(0,8))
        for c in range(4): lf_t.columnconfigure(c, weight=1)

        ttk.Label(lf_t, text="Position 1").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.b_pos1 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.b_pos1).grid(row=0, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(1, 1)).grid(row=0, column=2, padx=8)

        ttk.Label(lf_t, text="Position 2").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.b_pos2 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.b_pos2).grid(row=1, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(1, 2)).grid(row=1, column=2, padx=8)

        lf_tm = ttk.LabelFrame(f, text="Timing & Movement")
        lf_tm.grid(row=1, column=0, sticky="ew", pady=(0,8))
        for c in range(6): lf_tm.columnconfigure(c, weight=1)

        ttk.Label(lf_tm, text="Fixed wait after Space (s)").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.b_wait = tk.DoubleVar(value=self.bolts.fixed_wait)
        ttk.Spinbox(lf_tm, from_=0.0, to=999.0, increment=0.1, textvariable=self.b_wait, width=8)\
            .grid(row=0, column=1, sticky="w")

        ttk.Label(lf_tm, text="Move min (s)").grid(row=0, column=2, sticky="w", padx=8, pady=6)
        self.b_move_min = tk.DoubleVar(value=self.bolts.move_min)
        ttk.Spinbox(lf_tm, from_=0.0, to=5.0, increment=0.05, textvariable=self.b_move_min, width=8)\
            .grid(row=0, column=3, sticky="w")

        ttk.Label(lf_tm, text="Move max (s)").grid(row=0, column=4, sticky="w", padx=8, pady=6)
        self.b_move_max = tk.DoubleVar(value=self.bolts.move_max)
        ttk.Spinbox(lf_tm, from_=0.0, to=5.0, increment=0.05, textvariable=self.b_move_max, width=8)\
            .grid(row=0, column=5, sticky="w")

        ttk.Label(lf_tm, text="Jitter ± px").grid(row=1, column=0, sticky="w", padx=8, pady=(6,8))
        self.b_jitter = tk.IntVar(value=self.bolts.jitter)
        ttk.Spinbox(lf_tm, from_=0, to=100, increment=1, textvariable=self.b_jitter, width=8)\
            .grid(row=1, column=1, sticky="w")

        ttk.Label(lf_tm, text="Path style").grid(row=1, column=2, sticky="w", padx=8, pady=(6,8))
        self.b_path_style = tk.StringVar(value=self.bolts.path_style)
        ttk.Combobox(lf_tm, textvariable=self.b_path_style, values=["Straight","Mild","Natural"],
                     width=10, state="readonly").grid(row=1, column=3, sticky="w")

        ttk.Label(lf_tm, text="Engine").grid(row=1, column=4, sticky="w", padx=8, pady=(6,8))
        self.b_engine = tk.StringVar(value=self.bolts.engine)
        ttk.Combobox(lf_tm, textvariable=self.b_engine, values=["Fast","Smooth"], width=10, state="readonly")\
            .grid(row=1, column=5, sticky="w")

        ctl = ttk.Frame(f)
        ctl.grid(row=2, column=0, sticky="ew", pady=(0,8))
        ctl.columnconfigure(0, weight=1)
        ctl.columnconfigure(1, weight=1)
        ttk.Button(ctl, text="Start", command=lambda: self._start_tab(1)).grid(row=0, column=0, sticky="ew", padx=(0,4))
        ttk.Button(ctl, text="Stop",  command=lambda: self._stop_tab(1)).grid(row=0, column=1, sticky="ew", padx=(4,0))

        self.b_status = tk.StringVar(value="Idle  |  F8 = Start/Pause   Esc = Exit")
        ttk.Label(f, textvariable=self.b_status).grid(row=3, column=0, sticky="w")
        ttk.Label(f, text="Emergency stop: move mouse to top-left corner").grid(row=4, column=0, sticky="w")

    # Pickers, syncing, start/stop
    def _pick(self, tab_index: int, which: int):
        self.root.withdraw()
        try:
            for i in range(3, 0, -1):
                print(f"[dartmake] Hover over target (tab {tab_index}, pos {which}) ... {i}")
                time.sleep(1)
            pos = pyautogui.position()
        finally:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

        if tab_index == 0:
            if which == 1:
                self.darts.pos1 = (pos.x, pos.y)
                self.d_pos1.set(f"{pos.x}, {pos.y}")
            else:
                self.darts.pos2 = (pos.x, pos.y)
                self.d_pos2.set(f"{pos.x}, {pos.y}")
        else:
            if which == 1:
                self.bolts.pos1 = (pos.x, pos.y)
                self.b_pos1.set(f"{pos.x}, {pos.y}")
            else:
                self.bolts.pos2 = (pos.x, pos.y)
                self.b_pos2.set(f"{pos.x}, {pos.y}")
        print(f"[dartmake] Set Tab {tab_index} Pos {which}: {pos.x}, {pos.y}")

    def _sync_tab(self, idx: int):
        if idx == 0:
            b = self.darts
            b.min_delay  = float(self.d_min_delay.get())
            b.max_delay  = float(self.d_max_delay.get())
            b.move_min   = float(self.d_move_min.get())
            b.move_max   = float(self.d_move_max.get())
            b.jitter     = int(self.d_jitter.get())
            b.path_style = self.d_path_style.get()
            b.engine     = self.d_engine.get()
        else:
            b = self.bolts
            b.fixed_wait = float(self.b_wait.get())
            b.move_min   = float(self.b_move_min.get())
            b.move_max   = float(self.b_move_max.get())
            b.jitter     = int(self.b_jitter.get())
            b.path_style = self.b_path_style.get()
            b.engine     = self.b_engine.get()

    def _start_tab(self, idx: int):
        # Pause the other bot
        self._stop_tab(1 - idx, quiet=True)
        # Sync settings and sanity check
        self._sync_tab(idx)
        bot = self.bots[idx]
        if not (bot.pos1 and bot.pos2):
            messagebox.showwarning("dartmake", "Pick both positions on this tab.")
            return
        if bot.move_min > bot.move_max:
            bot.move_min, bot.move_max = bot.move_max, bot.move_min
        if hasattr(bot, "min_delay") and hasattr(bot, "max_delay") and bot.min_delay > bot.max_delay:
            bot.min_delay, bot.max_delay = bot.max_delay, bot.min_delay
        bot.start()

    def _stop_tab(self, idx: int, quiet: bool=False):
        self.bots[idx].pause()
        if not quiet:
            self._set_running_ui(idx, False)

    # Status + UI
    def _set_status(self, tab_index: int, text: str):
        if tab_index == 0:
            self.d_status.set(text)
        else:
            self.b_status.set(text)

    def _set_running_ui(self, tab_index: int, running: bool):
        if tab_index == 0:
            self.d_status.set("Running" if running else "Paused")
        else:
            self.b_status.set("Running" if running else "Paused")

    # Hotkeys
    def _listen_hotkeys(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f8:
                    idx = self.tabs.index(self.tabs.select())
                    self._stop_tab(1 - idx, quiet=True)
                    self._sync_tab(idx)
                    running = self.bots[idx].toggle()
                    self._set_running_ui(idx, running)
                elif key == keyboard.Key.esc:
                    for b in self.bots:
                        b.exit()
                    self.root.quit()
                    return False
            except Exception:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def on_close(self):
        for b in self.bots:
            b.exit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# ---------------- Entry ----------------
if __name__ == "__main__":
    App().run()
