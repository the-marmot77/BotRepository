from PIL import ImageGrab
from functools import partial
import pyautogui
import time
import random

# Configure ImageGrab to capture all screens
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Define the RGB values for the colors you want to click
purple_color = (144, 0, 173)  # Example RGB for purple
white_color = (255, 255, 255)  # RGB for white


def find_color_position(color, tolerance=10):
    """Find the position of a given color on the screen."""
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")
    for x in range(0, width, int(width/15)):  # Step by 100 pixels horizontally
        for y in range(int(height/2), height, 100):  # Step by 100 pixels vertically
            current_color = pyautogui.pixel(x, y)
            if pyautogui.pixelMatchesColor(x, y, color, tolerance=tolerance):
                print(
                    f"Matching color found at ({x}, {y}) with current_color: {current_color}"
                )
                return (x, y)
            else:
                print(f"No match at ({x}, {y}) - Current color: {current_color}")
    return None


def click_color(color, tolerance=10):
    """Find and click the given color on the screen with random offset."""
    pos = find_color_position(color, tolerance)
    if pos:
        # Apply random offsets to the detected position
        offset_x = random.randint(0, 25)
        offset_y = random.randint(0, 25)
        new_pos = (pos[0] + offset_x, pos[1] + offset_y)

        pyautogui.moveTo(new_pos, duration=random.uniform(0.3, 1.0))
        pyautogui.keyDown("shift")
        pyautogui.click(new_pos)
        pyautogui.keyUp("shift")
        print(
            f"Clicked on color at position {new_pos} with offsets ({offset_x}, {offset_y})."
        )
        time.sleep(
            random.uniform(0.5, 1.5)
        )  # Pause for a random interval between clicks
    else:
        
        print(f"Could not locate the color {color} on the screen.")


def click_logs_image():
    """Click on the logs image."""
    icon1 = pyautogui.locateCenterOnScreen("Logs2.PNG", confidence=0.9)
    if icon1:
        pyautogui.moveTo(icon1, duration=random.uniform(0.3, 1.0))
        pyautogui.click(icon1)
        print(f"Clicked on 'Logs.PNG' at position {icon1}.")
        time.sleep(
            random.uniform(0.5, 1.5)
        )  # Pause for a random interval after clicking

        icon2 = pyautogui.locateCenterOnScreen("XButton2.PNG", confidence=0.8)
        if icon2:
            pyautogui.moveTo(icon2, duration=random.uniform(0.3, 1.0))
            pyautogui.click(icon2)
            print(f"Clicked on 'XButton.PNG' at position {icon2}.")
            time.sleep(
                random.uniform(0.5, 1.5)
            )  # Pause for a random interval after clicking
    else:
        print(f"Could not locate 'Logs.PNG'.")

def move_to_random():
    x, y = pyautogui.size()
    randX = random.uniform(x, 1)
    randY = random.uniform(y, 1)
    pyautogui.moveTo(randX, randY, duration=random.uniform(0, 3))


def click_colors_and_image_in_order():
    """Click on the defined colors and image sequentially on the screen."""
    move_to_random()
    click_color(purple_color)
    move_to_random()
    click_logs_image()
    move_to_random()
    click_color(white_color)
    pyautogui.press("space")


if __name__ == "__main__":
    for i in range(10):  # Loop 10 times
        print(f"Iteration {i+1}")
        click_colors_and_image_in_order()
        time.sleep(random.uniform(70, 75))  # Random pause between iterations
    print("Completed 10 iterations.")
