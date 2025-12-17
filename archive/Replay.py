import pyautogui as auto
import random as r

def move_to_random():
    x, y = auto.size()
    randX = r.uniform(x, 1)
    randY = r.uniform(y, 1)
    print(randX, randY)

if __name__ == "__main__":
    move_to_random()