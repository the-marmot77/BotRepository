import pyautogui as pg

inv = pg.locateAllOnScreen("Rapid.png", confidence=0.7)

if inv:
    print("s")
else:
    print("f")

