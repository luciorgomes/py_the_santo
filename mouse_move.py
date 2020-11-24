import pyautogui
from pynput import keyboard
from pynput.mouse import Controller as MouseController
import random

def move_mouse():
    pyautogui.FAILSAFE = False

    mouse = MouseController()

    while True:
        turn = random.randint(-50, 50)
        with keyboard.Events() as events:
            # Block at most one second
            event = events.get(1.0)
            if event is not None:
                print('Interrompido!')
                break
            else:
                move = random.randint(-10, 10)
                pyautogui.move(- move, - move, duration=.10)
                pyautogui.move(turn, - turn, duration=.10)
                pyautogui.moveRel(move, turn, duration=.10)


if __name__ == '__main__':
    move_mouse()