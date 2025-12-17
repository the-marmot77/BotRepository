from .ui import AppUI
from .hotkeys import HotkeyManager


def main():
    app = AppUI()
    hk = HotkeyManager(toggle_active=app.toggle_active, exit_all=app.exit_all)
    hk.start()
    app.run()


if __name__ == "__main__":
    main()
