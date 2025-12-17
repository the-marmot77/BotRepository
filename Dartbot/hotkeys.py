import threading
from pynput import keyboard


class HotkeyManager:
    """
    Global hotkeys: F8 = toggle active tab, Esc = exit all.
    You must pass callables: toggle_active(), exit_all()
    """

    def __init__(self, toggle_active, exit_all):
        self.toggle_active = toggle_active
        self.exit_all = exit_all
        self.thread = threading.Thread(target=self._listen, daemon=True)

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()

    def _listen(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f8:
                    self.toggle_active()
                elif key == keyboard.Key.esc:
                    self.exit_all()
                    return False
            except Exception:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
