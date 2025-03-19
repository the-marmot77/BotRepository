import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import PlankMake  # Import the main bot script

bot_thread = None  # Track the bot execution thread

def start_bot(iterations_entry, min_delay_entry, max_delay_entry, status_label):
    global bot_thread
    iterations = int(iterations_entry.get())
    min_delay = float(min_delay_entry.get())
    max_delay = float(max_delay_entry.get())

    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(
            target=PlankMake.run_bot, args=(iterations, min_delay, max_delay), daemon=True
        )
        bot_thread.start()
        status_label.config(text="Status: Running", bootstyle="success")

def stop_bot(status_label):
    PlankMake.stop_bot()
    status_label.config(text="Status: Stopped", bootstyle="danger")

root = ttk.Window(themename="cyborg")  # Your preferred color scheme
root.title("PlankMake Bot")
root.geometry("400x250")

frame = ttk.Frame(root, padding="10")
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="Iterations:", bootstyle="inverse-dark").grid(row=0, column=0, sticky=ttk.W)
iterations_entry = ttk.Entry(frame, width=10, bootstyle="dark")
iterations_entry.grid(row=0, column=1)
iterations_entry.insert(0, "30")

ttk.Label(frame, text="Min Delay:", bootstyle="inverse-dark").grid(row=1, column=0, sticky=ttk.W)
min_delay_entry = ttk.Entry(frame, width=10, bootstyle="dark")
min_delay_entry.grid(row=1, column=1)
min_delay_entry.insert(0, "95")

ttk.Label(frame, text="Max Delay:", bootstyle="inverse-dark").grid(row=2, column=0, sticky=ttk.W)
max_delay_entry = ttk.Entry(frame, width=10, bootstyle="dark")
max_delay_entry.grid(row=2, column=1)
max_delay_entry.insert(0, "105")

start_button = ttk.Button(frame, text="Start Bot",
    command=lambda: start_bot(iterations_entry, min_delay_entry, max_delay_entry, status_label),
    bootstyle="success-outline")
start_button.grid(row=3, column=0, columnspan=2, pady=10)

stop_button = ttk.Button(frame, text="Stop Bot",
    command=lambda: stop_bot(status_label),
    bootstyle="danger-outline")
stop_button.grid(row=4, column=0, columnspan=2)

status_label = ttk.Label(frame, text="Status: Idle", bootstyle="inverse-dark")
status_label.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()
