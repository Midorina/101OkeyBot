import time
from threading import Thread

import keyboard
import pyautogui

pyautogui.PAUSE = 0


def get_current_mouse_coords():
    return pyautogui.position()


def move_mouse_to(coords):
    pyautogui.moveTo(coords)


def hold_click_while_carrying(coords1, coords2):
    pyautogui.mouseDown(*coords1)
    pyautogui.mouseUp(*coords2, duration=1.0)  # move the mouse to 100, 200, then release the button up.


def click(coords):
    pyautogui.moveTo(coords)
    pyautogui.click()



def rightclick(coords, after: float = None, block=True):
    if block is False:
        return Thread(target=rightclick, args=(coords, after)).start()
    else:
        if after:
            time.sleep(after)

        pyautogui.moveTo(coords)
        time.sleep(0.07)
        pyautogui.rightClick()


def press(button_name: str, after: float = None):
    if after:
        time.sleep(after)

    keyboard.press(button_name)
    time.sleep(0.1)
    keyboard.release(button_name)
