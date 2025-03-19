from PIL import ImageGrab
from functools import partial
import pyautogui
import time
import random
from pyclick import HumanClicker

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

purple_color = (144, 0, 173)

hc = HumanClicker()

def find_color_position(color, tolerance=10, step=250):
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")

    for x in range(0, width, step):
        for y in range(0, height, step):
            if pyautogui.pixelMatchesColor(x, y, color, tolerance=tolerance):
                print(f"Matching color found at ({x}, {y})")
                return (x, y)
    return None

def click_color(color, tolerance=10):
    pos = find_color_position(color, tolerance)
    if pos:
        offset_x, offset_y = random.randint(-10, 10), random.randint(-10, 10)
        new_pos = (pos[0] + offset_x, pos[1] + offset_y)

        hc.move(new_pos, duration=random.uniform(0.8, 2.0))
        pyautogui.keyDown("shift")
        pyautogui.click(new_pos)
        pyautogui.keyUp("shift")
        print(f"Clicked on color at {new_pos} with offsets ({offset_x}, {offset_y}).")
        time.sleep(random.uniform(0.5, 1.5))

def click_image(image_path, post_click=None, press_key=None, delay_after=(0.5, 1.5)):
    for _ in range(3):
        icon = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if icon:
            hc.move(icon, duration=random.uniform(0.8, 2.0))
            pyautogui.click(icon)
            print(f"Clicked on {image_path} at position {icon}.")
            time.sleep(random.uniform(*delay_after))

            if post_click:
                if isinstance(post_click, str):
                    post_click = [post_click]
                for extra_image in post_click:
                    extra_icon = pyautogui.locateCenterOnScreen(extra_image, confidence=0.8)
                    if extra_icon:
                        hc.move(extra_icon, duration=random.uniform(0.8, 2.0))
                        pyautogui.click(extra_icon)
                        print(f"Clicked on {extra_image} at position {extra_icon}.")
                        time.sleep(random.uniform(*delay_after))

            if press_key:
                pyautogui.press(press_key)
                print(f"Pressed key '{press_key}' after clicking {image_path}")

            return
        time.sleep(0.5)

    print(f"Failed to locate {image_path} after 3 attempts.")

def click_colors_and_image_in_order():
    click_color(purple_color)
    click_image("PlankMake\MahogPlank.png")
    click_image("PlankMake\MahogLog.png", post_click="PlankMake\XButton2.PNG")
    pyautogui.press("f4")
    time.sleep(random.uniform(0.1, 0.5))
    click_image("PlankMake\Spell1.PNG")
    click_image("PlankMake\MahogLog.PNG")
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.press("f1")

if __name__ == "__main__":
    for i in range(30):
        print(f"Iteration {i+1}")
        click_colors_and_image_in_order()
        time.sleep(random.uniform(95, 105))
    print("Completed all iterations.")
