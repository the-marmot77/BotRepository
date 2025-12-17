# BotRepository

Python utilities and GUI front-ends that automate a handful of RuneScape training activities.  The repository now has two polished, demonstrable projects plus an archive of earlier spikes.

## Repository map

| Path | Description |
| --- | --- |
| `Dartbot/` | Modern Tk/ttkbootstrap GUI (`dartmake`) that controls two pyautogui powered clicker bots (Darts and Bolts). |
| `PlankMake/` | Collection of RuneScape helpers: the plank-making loop with GUI, a Nightmare Zone prayer-flashing helper, an aerial fishing color bot, and a construction butler workflow. |
| `PlankMake/utilities/` | Screenshot + geometry helpers shared by the RuneScape scripts (MSS capture, template search, randomised click points). |
| `archive/` | Legacy automation experiments plus their image assets.  Not loaded by the active code. |
| `requirements.txt` | Minimal dependency list (pyautogui, pyclick, pynput, ttkbootstrap, numpy, Pillow, OpenCV, mss). |

## Setup

1. Use Python 3.11+ on Windows (pyautogui is configured for Windows hotkeys and fail-safe).
2. Create a virtual environment and install the dependencies:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Grant the process permission to control your mouse/keyboard if your OS prompts.  The scripts rely on `pyautogui.FAILSAFE`, so dragging the mouse to the top-left corner will immediately stop any running bot.

## Project details & functionality

### Dartbot (`Dartbot/`)

* **Purpose** - GUI hub for two precision clicker loops tailored to the `dartmake` minigame.  Users pick two screen coordinates per bot, tune timing/jitter/path-style, and control execution via buttons or global hotkeys.
* **Modules** - `movement.py` (bezier-style cursor motion), `bots.py` (threaded `BaseBot` plus `DartsBot` and `BoltsBot` implementations), `ui.py` (Tk/ttkbootstrap interface), `hotkeys.py` (pynput listeners), and `main.py` (entrypoint).
* **How to run** - From the repo root run `python -m Dartbot.main`.  The UI exposes two tabs, tooltips, and an emergency stop reminder.  Hotkeys: `F8` toggles the active tab, `Esc` stops both bots and exits.
* **Notable behavior** - Each bot jitters the selected coordinates, moves with either straight or natural wobble paths, enforces configurable delays, and surfaces status text back to the GUI.  The `movement` module provides easing + wobble logic in reusable helpers.

### RuneScape helpers (`PlankMake/`)

* **PlankMake bot** - `plankmake_bot.py` contains a `PlankMakeBot` class that scans for a purple NPC highlight, clicks mahogany planks/logs/spell icons via template matching, and alternates F4/F1 tabs.  `gui.py` wraps it in a ttkbootstrap interface (`python -m PlankMake` launches it).  The GUI validates numeric input, starts the bot in a background thread, and lets you stop gracefully.
* **Nightmare Zone helper** - `NMZ.py` flashes Rapid Heal every 30-36 seconds, periodically reboosts by clicking inventory potions, and reactivates prayers.  It relies on the utility template search for reliable clicks and logs each action.
* **Aerial fishing clicker** - `aerialfishing.py` searches for a magenta splash on the top half of the screen, performs saccade-like scans, and occasionally uses a knife on a bluegill icon found on the lower-right interface.
* **Construction butler script** - `ConstBot.py` color-scans the butler/bench, builds/removes teak benches in cycles, and pays the butler using `BotImages/ButlerPayment.png`.
* **Shared utilities** - `utilities/geometry.py` wraps MSS screen capture and rectangle math; `utilities/imagesearch.py` adds alpha-aware OpenCV template matching, and `utilities/random_util.py` generates human-like random points/timings.  The automation scripts import directly from these helpers to keep logic small.

### Archive (`archive/`)

The `archive/` folder now holds the raw prototypes: the original single-file `dartmake` GUI, first-pass plank make loops, auto-clickers, and their `.PNG` assets.  None of the production scripts import from this area, but you can cite it for historical context or experimentation.

## Usage notes

- **Assets** - All active scripts look for PNG assets in `PlankMake/BotImages/`.  Keep RuneLite in fixed positions or re-capture assets if the UI theme changes drastically.
- **Safety** - `pyautogui.FAILSAFE = True` is set everywhere.  Move your cursor to the top-left corner if you need to abort immediately.
- **Permissions** - Some scripts (e.g., NMZ helper) click function keys (`F4`, `F1`, `space`).  Close unrelated applications before running the bots to avoid unintended key presses.
- **Logging** - Each bot prints actions with a prefixed tag (`[plankmake]`, `[nmz]`, `[aerial]`) so you can tail the console and understand what is happening.

## Running individual tools

| Command | Result |
| --- | --- |
| `python -m Dartbot.main` | Launches the dartmake GUI with hotkeys (F8 / Esc). |
| `python -m PlankMake` or `python -m PlankMake.gui` | Opens the Plank Make helper GUI. |
| `python PlankMake/NMZ.py` | Runs the Rapid Heal / reboost helper until stopped. |
| `python PlankMake/aerialfishing.py` | Starts the aerial fishing color bot. |
| `python PlankMake/ConstBot.py` | Automates teak bench builds/removals with butler interactions. |

Feel free to highlight specific modules during interviews depending on the automation style you want to showcase.
