import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import PlankMake  # Import Plank Make script
import NMZ  # Import Nightmare Zone script
import ConstBot  # Import Construction script

bot_threads = {"PlankMake": None, "NightmareZone": None, "Construction": None}

def start_bot(script_name, script_module, input_entries, status_label):
    args = {}

    for key, entry in input_entries.items():
        if entry.get():
            try:
                args[key] = int(entry.get()) if entry.get().isdigit() else entry.get()
            except ValueError:
                args[key] = entry.get()

    if bot_threads[script_name] is None or not bot_threads[script_name].is_alive():
        bot_threads[script_name] = threading.Thread(
            target=script_module.run_bot, kwargs=args, daemon=True
        )
        bot_threads[script_name].start()
        status_label.config(text=f"Status: Running {script_name}", bootstyle="success")

def stop_bot(script_name, script_module, status_label):
    script_module.stop_bot()
    status_label.config(text=f"Status: Stopped {script_name}", bootstyle="danger")

root = ttk.Window(themename="cyborg")
root.title("OSRS Automation Bot")
root.geometry("400x350")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

def create_script_tab(tab_name, script_module, fields):
    frame = ttk.Frame(notebook, padding="10")
    notebook.add(frame, text=tab_name)

    input_entries = {}

    for i, (label, default_value) in enumerate(fields.items()):
        ttk.Label(frame, text=f"{label}:", bootstyle="inverse-dark").grid(row=i, column=0, sticky=ttk.W)
        entry = ttk.Entry(frame, width=10, bootstyle="dark")
        entry.grid(row=i, column=1)
        entry.insert(0, str(default_value))
        input_entries[label] = entry

    status_label = ttk.Label(frame, text="Status: Idle", bootstyle="inverse-dark")
    status_label.grid(row=len(fields) + 1, column=0, columnspan=2, pady=5)

    start_button = ttk.Button(frame, text="Start",
        command=lambda: start_bot(tab_name, script_module, input_entries, status_label),
        bootstyle="success-outline")
    start_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    stop_button = ttk.Button(frame, text="Stop",
        command=lambda: stop_bot(tab_name, script_module, status_label),
        bootstyle="danger-outline")
    stop_button.grid(row=len(fields) + 2, column=0, columnspan=2)

# Define unique fields for each script
plank_fields = {"Iterations": 30, "Min Delay": 95, "Max Delay": 105}
nmz_fields = {"Absorption Doses": 20, "Overload Doses": 5, "Prayer Flick": "False"}
construction_fields = {"Mode": "Mahogany", "Servant Name": "Demon Butler", "Iterations": 50}

create_script_tab("PlankMake", PlankMake, plank_fields)
create_script_tab("NightmareZone", NMZ, nmz_fields)
create_script_tab("Construction", ConstBot, construction_fields)

root.mainloop()
