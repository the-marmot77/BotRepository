from PIL import ImageGrab
from functools import partial
import pyautogui
import time
import random

# Configure ImageGrab to capture all screens
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Define the RGB value for the purple color
purple_color = (144, 0, 173)


def find_color_position(color, tolerance=10):
    """Find the position of a given color on the screen."""
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")
    for x in range(0, width, 150):  # Step by 150 pixels horizontally
        for y in range(0, height, 150):  # Step by 150 pixels vertically
            if pyautogui.pixelMatchesColor(x, y, color, tolerance=tolerance):
                print(f"Matching color found at ({x}, {y})")
                return (x, y)
    return None


def click_images(image):
    """Click on the provided image if found on screen, retrying up to 3 times."""
    for _ in range(3):
        icon = pyautogui.locateCenterOnScreen(image, confidence=0.8)
        if icon:
            pyautogui.moveTo(icon, duration=random.uniform(0.3, 1.0))
            pyautogui.click(icon)
            print(f"Clicked on {image} at position {icon}.")
            time.sleep(random.uniform(0.5, 1.5))
            return
        time.sleep(0.5)
    print(f"Failed to locate {image} after 3 attempts.")


def click_color(color, tolerance=10):
    """Find and click the given color on the screen with a slight offset."""
    pos = find_color_position(color, tolerance)
    if pos:
        offset_x, offset_y = random.randint(-10, 10), random.randint(-10, 10)
        new_pos = (pos[0] + offset_x, pos[1] + offset_y)

        pyautogui.moveTo(new_pos, duration=random.uniform(0.3, 1.0))
        pyautogui.keyDown("shift")
        pyautogui.click(new_pos)
        pyautogui.keyUp("shift")
        print(f"Clicked on color at {new_pos} with offsets ({offset_x}, {offset_y}).")
        time.sleep(random.uniform(0.5, 1.5))


def click_logs_image():
    """Click on the logs image and close the interface if found."""
    icon1 = pyautogui.locateCenterOnScreen("MahogLog.png", confidence=0.8)
    if icon1:
        pyautogui.moveTo(icon1, duration=random.uniform(0.3, 1.0))
        pyautogui.click(icon1)
        print(f"Clicked on 'MahogLog.PNG' at position {icon1}.")
        time.sleep(random.uniform(0.5, 1.5))

        icon2 = pyautogui.locateCenterOnScreen("XButton2.PNG", confidence=0.8)
        if icon2:
            pyautogui.moveTo(icon2, duration=random.uniform(0.3, 1.0))
            pyautogui.click(icon2)
            print(f"Clicked on 'XButton.PNG' at position {icon2}.")
            time.sleep(random.uniform(0.5, 1.5))


def click_spell_image():
    """Click on the spell image if found."""
    icon = pyautogui.locateCenterOnScreen("Spell1.PNG", confidence=0.9)
    if icon:
        pyautogui.moveTo(icon, duration=random.uniform(0.3, 1.0))
        pyautogui.click(icon)
        print(f"Clicked on 'Spell1.PNG' at position {icon}.")
        time.sleep(random.uniform(0.5, 1.5))


def click_colors_and_image_in_order():
    """Click on the defined colors and images sequentially."""
    click_color(purple_color)
    click_images("MahogPlank.png")
    click_logs_image()
    pyautogui.press("f4")
    click_spell_image()
    click_images("MahogLog.PNG")
    pyautogui.press("f1")


if __name__ == "__main__":
    for i in range(15):
        print(f"Iteration {i+1}")
        click_colors_and_image_in_order()
        time.sleep(random.uniform(95, 105))  # Random pause between iterations
    print("Completed 15 iterations.")
