from PIL import ImageGrab
from functools import partial
import pyautogui
import time

# Configure ImageGrab to capture all screens
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Define the RGB values for the colors you want to click
purple_color = (144, 0, 173)  # Example RGB for purple
white_color = (255, 255, 255)  # RGB for white


def find_color_position(color, tolerance=10):
    """Find the position of a given color on the screen."""
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")
    for x in range(0, width, 150):  # Step by 150 pixels horizontally
        for y in range(0, height, 150):  # Step by 150 pixels vertically
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
    """Find and click the given color on the screen."""
    pos = find_color_position(color, tolerance)
    if pos:
        pyautogui.moveTo(pos, duration=0.3)
        pyautogui.keyDown('shift')
        pyautogui.click(pos)
        pyautogui.keyUp('shift')
        print(f"Clicked on color at position {pos}.")
        time.sleep(2)  # Pause for 1 second between clicks
        
    else:
        print(f"Could not locate the color {color} on the screen.")


def click_logs_image():
    """Click on the logs image."""
    icon1 = pyautogui.locateCenterOnScreen("Logs.PNG", confidence=0.9)
    if icon1:
        pyautogui.moveTo(icon1, duration=0.3)
        pyautogui.click(icon1)
        print(f"Clicked on 'Logs.PNG' at position {icon1}.")
        time.sleep(2)  # Pause for 1 second after clicking

        icon2 = pyautogui.locateCenterOnScreen("XButton.PNG", confidence=0.5)
        if icon2:
            pyautogui.moveTo(icon2, duration=0.3)
            pyautogui.click(icon2)
            print(f"Clicked on 'XButton.PNG' at position {icon2}.")
            time.sleep(1)  # Pause for 1 second after clicking

    else:
        print(f"Could not locate 'Logs.PNG'.")


def click_colors_and_image_in_order():
    
    """Click on the defined colors and image sequentially on the screen."""
    click_color(purple_color)
    click_logs_image()
    click_color(white_color)
    pyautogui.press('space')


if __name__ == "__main__":
    for i in range(10):  # Loop 10 times
        print(f"Iteration {i+1}")
        click_colors_and_image_in_order()
        time.sleep(70)  # Optional pause between iterations
    print("Completed 10 iterations.")