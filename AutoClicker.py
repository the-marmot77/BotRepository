import pyautogui
import time
import datetime
import keyboard
import random

def auto_clicker(min_interval=1, max_interval=2):
    """
    Function to automate mouse clicks.
    
    :param min_interval: Minimum time (in seconds) to wait between clicks.
    :param max_interval: Maximum time (in seconds) to wait between clicks.
    """
    clicking = False
    print("Press 'Alt + R' to start and 'Esc' to stop the auto-clicker.")

    while True:
        if not clicking:
            keyboard.wait('alt+r')  # Waits until 'Alt + R' is pressed and released
            clicking = True
            print("\nAuto-clicker started.")

        while clicking:
            if keyboard.is_pressed('esc'):
                clicking = False
                time.sleep(0.2)  # Brief pause to ensure 'esc' is not immediately re-detected
                print("\nAuto-clicker stopped.")
                break

            start_time = time.time()

            wait_duration = 250

            boost_time = time.time() - start_time

            if boost_time >= wait_duration:
                # Actions to reboost
            
            # Perform two clicks
            pyautogui.click()
            pyautogui.click()
            interval = random.uniform(min_interval, max_interval)
            time.sleep(interval)

            

if __name__ == "__main__":
    min_interval = float(input("Enter the minimum time interval (in seconds) between clicks: "))
    max_interval = float(input("Enter the maximum time interval (in seconds) between clicks: "))
    
    if min_interval > max_interval:
        print("Minimum interval should be less than or equal to Maximum interval.")
    else:
        auto_clicker(min_interval, max_interval)
