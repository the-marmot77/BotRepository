import pyautogui, sys
import time
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
    
    target_time = time.time() + 15

    while True:
        if not clicking:
            keyboard.wait('alt+r')  # Waits until 'Alt + R' is pressed and released
            clicking = True
            time.sleep(0.2)
            print("\nAuto-clicker started.")

        while clicking:
            
            try:
                InventoryTab = pyautogui.locateOnScreen('TabBar.png')
                
            except pyautogui.ImageNotFoundException:
                print('Unable to loacate inventory tab...')
                continue
                
            boost_time = target_time - time.time()

            if boost_time <= 0:
                # Actions to boost again
                pyautogui.click(InventoryTab)
                target_time = time.time() + 15

            interval = random.uniform(min_interval, max_interval)
            pyautogui.doubleClick(interval=0.1)
            time.sleep(interval)
            
            # Make another random interval here for time between clicks/

            

if __name__ == "__main__":
    min_interval = float(input("Enter the minimum time interval (in seconds) between clicks: "))
    max_interval = float(input("Enter the maximum time interval (in seconds) between clicks: "))
    
    if min_interval > max_interval:
        print("Minimum interval should be less than or equal to Maximum interval.")
    else:
        auto_clicker(min_interval, max_interval)
