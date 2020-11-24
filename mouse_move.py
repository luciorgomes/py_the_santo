import pyautogui
from pynput import keyboard
import random

def move_mouse():
    pyautogui.FAILSAFE = False

    while True:
        with keyboard.Events() as events:
            # Block at most one second
            event = events.get(0.5)
            if event is not None:
                print('Interrompido!')
                break
            else:
                move = random.randint(-10, 10)
                pyautogui.move(move, move, duration=.03)
                pyautogui.move(- move, move, duration=.03)
                pyautogui.move(- move, - move, duration=.03)
                pyautogui.move(move, - move, duration=.03)


if __name__ == '__main__':
    move_mouse()