import pyautogui
import json
import time

# Load the recorded events from the file
with open('recorded_events.json', 'r') as f:
    recorded_events = json.load(f)

# Replay the recorded events
for event in recorded_events:
    event_type = event[0]
    if event_type == 'move':
        _, x, y = event
        pyautogui.moveTo(x, y)
    elif event_type == 'pressed':
        _, x, y, button = event
        if button == 'Button.left':
            pyautogui.mouseDown(x, y, button='left')
        elif button == 'Button.right':
            pyautogui.mouseDown(x, y, button='right')
    elif event_type == 'released':
        _, x, y, button = event
        if button == 'Button.left':
            pyautogui.mouseUp(x, y, button='left')
        elif button == 'Button.right':
            pyautogui.mouseUp(x, y, button='right')
    elif event_type == 'scroll':
        _, x, y, dx, dy = event
        pyautogui.scroll(dy, x, y)
    
    # Small delay to make the replay realistic but fast
    time.sleep(0.01)
