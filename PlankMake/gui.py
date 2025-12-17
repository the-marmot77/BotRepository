from __future__ import annotations

import threading
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import W

from .plankmake_bot import run_bot, stop_bot


class PlankMakeGUI:
    """Simple ttkbootstrap front-end for the plank maker bot."""

    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self.root = ttk.Window(themename="cyborg")
        self.root.title("Plank Make Bot")
        self.root.geometry("360x240")
        self._build_form()

    def _build_form(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Iterations:", bootstyle="inverse-dark").grid(
            row=0, column=0, sticky=W
        )
        self.iterations_entry = ttk.Entry(frame, width=10, bootstyle="dark")
        self.iterations_entry.grid(row=0, column=1, padx=(8, 0))
        self.iterations_entry.insert(0, "30")

        ttk.Label(frame, text="Min Delay (s):", bootstyle="inverse-dark").grid(
            row=1, column=0, sticky=W
        )
        self.min_delay_entry = ttk.Entry(frame, width=10, bootstyle="dark")
        self.min_delay_entry.grid(row=1, column=1, padx=(8, 0))
        self.min_delay_entry.insert(0, "95")

        ttk.Label(frame, text="Max Delay (s):", bootstyle="inverse-dark").grid(
            row=2, column=0, sticky=W
        )
        self.max_delay_entry = ttk.Entry(frame, width=10, bootstyle="dark")
        self.max_delay_entry.grid(row=2, column=1, padx=(8, 0))
        self.max_delay_entry.insert(0, "105")

        ttk.Button(
            frame,
            text="Start",
            command=self._on_start,
            bootstyle="success-outline",
        ).grid(row=3, column=0, columnspan=2, pady=(16, 6), sticky="ew")

        ttk.Button(
            frame,
            text="Stop",
            command=self._on_stop,
            bootstyle="danger-outline",
        ).grid(row=4, column=0, columnspan=2, sticky="ew")

        self.status = ttk.Label(frame, text="Status: Idle", bootstyle="inverse-dark")
        self.status.grid(row=5, column=0, columnspan=2, pady=(12, 0), sticky=W)

    def _on_start(self) -> None:
        try:
            iterations = int(self.iterations_entry.get())
            min_delay = float(self.min_delay_entry.get())
            max_delay = float(self.max_delay_entry.get())
        except ValueError:
            messagebox.showerror("Plank Make Bot", "Enter numeric values for all fields.")
            return

        if iterations <= 0:
            messagebox.showwarning("Plank Make Bot", "Iterations must be positive.")
            return

        if self._thread and self._thread.is_alive():
            messagebox.showinfo("Plank Make Bot", "Bot already running.")
            return

        self._thread = threading.Thread(
            target=run_bot, args=(iterations, min_delay, max_delay), daemon=True
        )
        self._thread.start()
        self.status.config(text="Status: Running", bootstyle="success")

    def _on_stop(self) -> None:
        stop_bot()
        self.status.config(text="Status: Stopped", bootstyle="danger")

    def run(self) -> None:
        self.root.mainloop()


def launch() -> None:
    PlankMakeGUI().run()


if __name__ == "__main__":
    launch()
