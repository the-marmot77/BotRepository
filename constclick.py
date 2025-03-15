import pyautogui
import time

def repeat_actions(delay=1, repetitions=50):
    """
    Repeats the sequence of actions: 
    1. Left mouse click
    2. Wait
    3. Press '3'
    4. Wait
    5. Left mouse click
    6. Press '1'
    
    :param delay: Time to wait between actions (in seconds)
    :param repetitions: Number of times to repeat the sequence
    """
    count = 0  # Initialize count inside the function
    for _ in range(repetitions):
        pyautogui.click()  # Left mouse button click
        time.sleep(delay)  # Wait
        
        pyautogui.press('3')  # Press the '3' key
        time.sleep(1.5)  # Wait
        
        pyautogui.click()  # Left mouse button click
        time.sleep(delay)  # Wait
        
        pyautogui.press('1')  # Press the '1' key
        time.sleep(1.5)  # Wait
        
        count += 1
        print(f"{count} repetition(s) completed")  # Use f-strings for clarity

if __name__ == "__main__":
    try:
        delay_between_actions = 1  # Set delay between actions
        number_of_repeats = 50  # Set number of repetitions
        
        print(f"Starting... Script will repeat {number_of_repeats} times with a {delay_between_actions}s delay.")
        time.sleep(3)  # Give user time to prepare
        repeat_actions(delay=delay_between_actions, repetitions=number_of_repeats)
        print("Finished.")
    except KeyboardInterrupt:
        print("Script stopped by user.")
