from pyclick import HumanClicker
import time

hc = HumanClicker()

i = 0

while i != 10:
    
    if (i % 2 == 0):
        
        hc.move((100,100),2)
        print(i)
        i += 1
        time.sleep(1)

    else:

        hc.move((650, 650), 2)
        print(i)
        i += 1
        time.sleep(1)