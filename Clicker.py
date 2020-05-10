import time
import threading
from pynput.mouse import Button as pButton, Controller
from pynput.keyboard import Listener, KeyCode
import pyautogui as pg
from tkinter import *

xx, yy = 0, 0
delay = 1
button = pButton.left
start_stop_key = KeyCode(char=  "s")
exit_key = KeyCode(char = "e")

def update_delay():
    try:
        global delay
        delay = float(Entry_delay.get())
        # print(delay)
    except ValueError:
        print("Error")


def start_clicker():
    class ClickMouse(threading.Thread):
        def __init__(self, delay, button):
            super(ClickMouse, self).__init__()
            self.delay = delay
            self.button = button
            self.running = False
            self.program_running = True

        def start_clicking(self):
            self.running = True

        def stop_clicking(self):
            self.running = False

        def exit(self):
            self.stop_clicking()
            self.program_running = False

        def run(self):
            while self.program_running:
                while self.running:
                    old_position = pg.position()
                    x_old, y_old = old_position
                    x, y = position
                    pg.moveTo(x,y)
                    mouse.click(self.button)
                    pg.moveTo(x_old, y_old)
                    time.sleep(self.delay)
                time.sleep(0.1)


    mouse = Controller()
    click_thread = ClickMouse(delay, button)
    click_thread.start()


    def on_press(key):
        if key == start_stop_key:
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                global position
                position = pg.position()
                click_thread.start_clicking()

        elif key == exit_key:
            click_thread.exit()
            listener.stop()


    with Listener(on_press=on_press) as listener:
        listener.join()



frame = Tk()
frame.title("AutoClicker")
frame.geometry("200x200")
frame.configure(background='#76EEC6')
labelSteps = Label(frame, bg="#FFCFC9", text="Update delay in seconds")
labelSteps.pack()
Entry_delay = Entry(frame, bg="white")
Entry_delay.pack()
button_update = Button(frame, text="update", command = update_delay)
button_update.pack()
labelStart = Label(frame, bg="#FFCFC9", text="Start-Stop key: s")
labelStart.pack()
labelEnd = Label(frame, bg="#FFCFC9", text="Exit key: e")
labelEnd.pack()
button_start = Button(frame, text="start", command = start_clicker)
button_start.pack()
frame.mainloop()