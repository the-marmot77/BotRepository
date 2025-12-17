import time
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui

try:
    import ttkbootstrap as tb

    HAS_BOOTSTRAP = True
except Exception:
    HAS_BOOTSTRAP = False

from .bots import DartsBot, BoltsBot

pyautogui.FAILSAFE = True


class AppUI:
    """
    Builds the GUI and owns the bots.
    Exposes: start_tab(i), stop_tab(i), toggle_active(), exit_all(), active_index()
    """

    def __init__(self):
        self.root = tb.Window(themename="cyborg") if HAS_BOOTSTRAP else tk.Tk()
        self.root.title("dartmake")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.darts = DartsBot()
        self.bolts = BoltsBot()
        self.bots = [self.darts, self.bolts]

        # UI callbacks
        self.darts.on_status = lambda s: self._set_status(0, s)
        self.bolts.on_status = lambda s: self._set_status(1, s)
        self.darts.on_running_changed = lambda r: self._set_running_ui(0, r)
        self.bolts.on_running_changed = lambda r: self._set_running_ui(1, r)

        # Layout
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.tabs = ttk.Notebook(main)
        self.tabs.grid(row=0, column=0, sticky="nsew")

        self._build_darts_tab()
        self._build_bolts_tab()

        # Ensure worker threads exist
        for b in self.bots:
            b.ensure_thread()

    # ---------- public controls for hotkeys ----------
    def active_index(self) -> int:
        return self.tabs.index(self.tabs.select())

    def toggle_active(self):
        idx = self.active_index()
        # pause the other bot for exclusivity
        self.stop_tab(1 - idx, quiet=True)
        self._sync_tab(idx)
        running = self.bots[idx].toggle()
        self._set_running_ui(idx, running)

    def exit_all(self):
        for b in self.bots:
            b.exit()
        self.root.quit()

    def start_tab(self, idx: int):
        self.stop_tab(1 - idx, quiet=True)
        self._sync_tab(idx)
        bot = self.bots[idx]
        if not (bot.pos1 and bot.pos2):
            messagebox.showwarning("dartmake", "Pick both positions on this tab.")
            return
        if bot.move_min > bot.move_max:
            bot.move_min, bot.move_max = bot.move_max, bot.move_min
        if (
            hasattr(bot, "min_delay")
            and hasattr(bot, "max_delay")
            and bot.min_delay > bot.max_delay
        ):
            bot.min_delay, bot.max_delay = bot.max_delay, bot.min_delay
        bot.start()

    def stop_tab(self, idx: int, quiet: bool = False):
        self.bots[idx].pause()
        if not quiet:
            self._set_running_ui(idx, False)

    # ---------- UI build ----------
    def _build_darts_tab(self):
        f = ttk.Frame(self.tabs)
        self.tabs.add(f, text="Darts")

        # Targets
        lf_t = ttk.LabelFrame(f, text="Targets")
        lf_t.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        for c in range(3):
            lf_t.columnconfigure(c, weight=1)

        ttk.Label(lf_t, text="Position 1").grid(
            row=0, column=0, sticky="w", padx=8, pady=6
        )
        self.d_pos1 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.d_pos1).grid(row=0, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(0, 1)).grid(
            row=0, column=2, padx=8
        )

        ttk.Label(lf_t, text="Position 2").grid(
            row=1, column=0, sticky="w", padx=8, pady=6
        )
        self.d_pos2 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.d_pos2).grid(row=1, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(0, 2)).grid(
            row=1, column=2, padx=8
        )

        # Timing & Movement
        lf_tm = ttk.LabelFrame(f, text="Timing & Movement")
        lf_tm.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for c in range(4):
            lf_tm.columnconfigure(c, weight=1)

        ttk.Label(lf_tm, text="Delay min (s)").grid(
            row=0, column=0, sticky="w", padx=8, pady=6
        )
        self.d_min_delay = tk.DoubleVar(value=self.darts.min_delay)
        ttk.Spinbox(
            lf_tm,
            from_=0.0,
            to=999.0,
            increment=0.1,
            textvariable=self.d_min_delay,
            width=8,
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(lf_tm, text="Delay max (s)").grid(
            row=0, column=2, sticky="w", padx=8, pady=6
        )
        self.d_max_delay = tk.DoubleVar(value=self.darts.max_delay)
        ttk.Spinbox(
            lf_tm,
            from_=0.0,
            to=999.0,
            increment=0.1,
            textvariable=self.d_max_delay,
            width=8,
        ).grid(row=0, column=3, sticky="w")

        ttk.Label(lf_tm, text="Move min (s)").grid(
            row=1, column=0, sticky="w", padx=8, pady=6
        )
        self.d_move_min = tk.DoubleVar(value=self.darts.move_min)
        ttk.Spinbox(
            lf_tm,
            from_=0.0,
            to=10.0,
            increment=0.05,
            textvariable=self.d_move_min,
            width=8,
        ).grid(row=1, column=1, sticky="w")

        ttk.Label(lf_tm, text="Move max (s)").grid(
            row=1, column=2, sticky="w", padx=8, pady=6
        )
        self.d_move_max = tk.DoubleVar(value=self.darts.move_max)
        ttk.Spinbox(
            lf_tm,
            from_=0.0,
            to=10.0,
            increment=0.05,
            textvariable=self.d_move_max,
            width=8,
        ).grid(row=1, column=3, sticky="w")

        ttk.Label(lf_tm, text="Jitter (px)").grid(
            row=2, column=0, sticky="w", padx=8, pady=(6, 8)
        )
        self.d_jitter = tk.IntVar(value=self.darts.jitter)
        ttk.Spinbox(
            lf_tm, from_=0, to=100, increment=1, textvariable=self.d_jitter, width=8
        ).grid(row=2, column=1, sticky="w")

        ttk.Label(lf_tm, text="Path style").grid(
            row=2, column=2, sticky="w", padx=8, pady=(6, 8)
        )
        self.d_path_style = tk.StringVar(value=self.darts.path_style)
        ttk.Combobox(
            lf_tm,
            textvariable=self.d_path_style,
            values=["Straight", "Mild", "Natural"],
            width=10,
            state="readonly",
        ).grid(row=2, column=3, sticky="w")

        # Controls + Status
        ctl = ttk.Frame(f)
        ctl.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        ctl.columnconfigure(0, weight=1)
        ctl.columnconfigure(1, weight=1)
        ttk.Button(ctl, text="Start", command=lambda: self.start_tab(0)).grid(
            row=0, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(ctl, text="Stop", command=lambda: self.stop_tab(0)).grid(
            row=0, column=1, sticky="ew", padx=(4, 0)
        )

        self.d_status = tk.StringVar(value="Idle  |  F8 = Start/Pause   Esc = Exit")
        ttk.Label(f, textvariable=self.d_status).grid(row=3, column=0, sticky="w")
        ttk.Label(f, text="Emergency stop: move mouse to top-left corner").grid(
            row=4, column=0, sticky="w"
        )

    def _build_bolts_tab(self):
        f = ttk.Frame(self.tabs)
        self.tabs.add(f, text="Bolts")

        lf_t = ttk.LabelFrame(f, text="Targets")
        lf_t.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        for c in range(3):
            lf_t.columnconfigure(c, weight=1)

        ttk.Label(lf_t, text="Position 1").grid(
            row=0, column=0, sticky="w", padx=8, pady=6
        )
        self.b_pos1 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.b_pos1).grid(row=0, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(1, 1)).grid(
            row=0, column=2, padx=8
        )

        ttk.Label(lf_t, text="Position 2").grid(
            row=1, column=0, sticky="w", padx=8, pady=6
        )
        self.b_pos2 = tk.StringVar(value="Not set")
        ttk.Label(lf_t, textvariable=self.b_pos2).grid(row=1, column=1, sticky="w")
        ttk.Button(lf_t, text="Pick", command=lambda: self._pick(1, 2)).grid(
            row=1, column=2, padx=8
        )

        lf_tm = ttk.LabelFrame(f, text="Timing & Movement")
        lf_tm.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for c in range(4):
            lf_tm.columnconfigure(c, weight=1)

        ttk.Label(lf_tm, text="Fixed wait after Space (s)").grid(
            row=0, column=0, sticky="w", padx=8, pady=6
        )
        self.b_wait = tk.DoubleVar(value=self.bolts.fixed_wait)
        ttk.Spinbox(
            lf_tm, from_=0.0, to=999.0, increment=0.1, textvariable=self.b_wait, width=8
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(lf_tm, text="Move min (s)").grid(
            row=0, column=2, sticky="w", padx=8, pady=6
        )
        self.b_move_min = tk.DoubleVar(value=self.bolts.move_min)
        ttk.Spinbox(
            lf_tm,
            from_=0.0,
            to=10.0,
            increment=0.05,
            textvariable=self.b_move_min,
            width=8,
        ).grid(row=0, column=3, sticky="w")

        ttk.Label(lf_tm, text="Move max (s)").grid(
            row=1, column=2, sticky="w", padx=8, pady=6
        )
        self.b_move_max = tk.DoubleVar(value=self.bolts.move_max)
        ttk.Spinbox(
            lf_tm,
            from_=0.0,
            to=10.0,
            increment=0.05,
            textvariable=self.b_move_max,
            width=8,
        ).grid(row=1, column=3, sticky="w")

        ttk.Label(lf_tm, text="Jitter (px)").grid(
            row=1, column=0, sticky="w", padx=8, pady=(6, 8)
        )
        self.b_jitter = tk.IntVar(value=self.bolts.jitter)
        ttk.Spinbox(
            lf_tm, from_=0, to=100, increment=1, textvariable=self.b_jitter, width=8
        ).grid(row=1, column=1, sticky="w")

        ttk.Label(lf_tm, text="Path style").grid(
            row=2, column=0, sticky="w", padx=8, pady=(6, 8)
        )
        self.b_path_style = tk.StringVar(value=self.bolts.path_style)
        ttk.Combobox(
            lf_tm,
            textvariable=self.b_path_style,
            values=["Straight", "Mild", "Natural"],
            width=10,
            state="readonly",
        ).grid(row=2, column=1, sticky="w")

        ctl = ttk.Frame(f)
        ctl.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        ctl.columnconfigure(0, weight=1)
        ctl.columnconfigure(1, weight=1)
        ttk.Button(ctl, text="Start", command=lambda: self.start_tab(1)).grid(
            row=0, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(ctl, text="Stop", command=lambda: self.stop_tab(1)).grid(
            row=0, column=1, sticky="ew", padx=(4, 0)
        )

        self.b_status = tk.StringVar(value="Idle  |  F8 = Start/Pause   Esc = Exit")
        ttk.Label(f, textvariable=self.b_status).grid(row=3, column=0, sticky="w")
        ttk.Label(f, text="Emergency stop: move mouse to top-left corner").grid(
            row=4, column=0, sticky="w"
        )

    # ---------- pickers, syncing, status ----------
    def _pick(self, tab_index: int, which: int):
        # Hide window during capture
        self.root.withdraw()
        try:
            for i in range(3, 0, -1):
                print(
                    f"[dartmake] Hover over target (tab {tab_index}, pos {which}) ... {i}"
                )
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

    def _sync_tab(self, tab_index: int):
        if tab_index == 0:
            b = self.darts
            b.min_delay = float(self.d_min_delay.get())
            b.max_delay = float(self.d_max_delay.get())
            b.move_min = float(self.d_move_min.get())
            b.move_max = float(self.d_move_max.get())
            b.jitter = int(self.d_jitter.get())
            b.path_style = self.d_path_style.get()
        else:
            b = self.bolts
            b.fixed_wait = float(self.b_wait.get())
            b.move_min = float(self.b_move_min.get())
            b.move_max = float(self.b_move_max.get())
            b.jitter = int(self.b_jitter.get())
            b.path_style = self.b_path_style.get()

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

    # ---------- shutdown ----------
    def on_close(self):
        self.exit_all()

    # ---------- mainloop ----------
    def run(self):
        self.root.mainloop()
