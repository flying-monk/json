import pyautogui as pg
import time

print("Irritation starts in 5 seconds")
time.sleep(5)

for i in range(50):
    pg.write("Hi, trushant")
    time.sleep(0.5)
    pg.press("Enter")