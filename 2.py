import time
import ctypes
import os
import mss
from colorama import Fore, Style, init
from PIL import ImageGrab, Image
import winsound
import keyboard

S_HEIGHT, S_WIDTH = ImageGrab.grab().size
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 31
GRABZONE = 10
TRIGGER_KEY = "ctrl + alt"
SWITCH_KEY = "ctrl + tab"
GRABZONE_KEY_UP = "ctrl + up"
BUNNY_KEY = "ctrl + space"
GRABZONE_KEY_DOWN = "ctrl + down"
mods = ["OPERATOR/MARSHAL", "GUARDIAN", "VANDAL/PHANTOM/SHOTGUNS"]
ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up

class FoundEnemy(Exception):
    pass

class TriggerBot:
    def __init__(self):
        self.toggled = False
        self._bunny = False
        self.mode = 1
        self.last_reac = 0
        self.last_click_time = 0

    def toggle(self):
        self.toggled = not self.toggled

    def bunny(self):
        self._bunny = not self._bunny

    def switch(self):
        if self.mode != 2:
            self.mode += 1
        else:
            self.mode = 0
        if self.mode == 0:
            winsound.Beep(200, 200)
        if self.mode == 1:
            winsound.Beep(200, 200), winsound.Beep(200, 200)
        if self.mode == 2:
            winsound.Beep(200, 200), winsound.Beep(200, 200), winsound.Beep(200, 200)

    def double_click(self):
        current_time = time.time()
        if current_time - self.last_click_time < 0.3:
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up
        self.last_click_time = current_time

    def approx(self, r, g, b):
        return (
            PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE
            and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE
            and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE
        )

    def grab(self):
        with mss.mss() as sct:
            bbox = (
                int(S_HEIGHT / 2 - GRABZONE),
                int(S_WIDTH / 2 - GRABZONE),
                int(S_HEIGHT / 2 + GRABZONE),
                int(S_WIDTH / 2 + GRABZONE),
            )
            img = sct.grab(bbox)
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            pixels = img.load()
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    r, g, b = pixels[i, j]
                    if self.approx(r, g, b):
                        raise FoundEnemy

    def print_banner(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(Fore.RED + "Ousmane Valorant TriggerBot v1.0.0" + Style.RESET_ALL)
        print("===== Control =====")
        print("Activation key        : " + TRIGGER_KEY)
        print("Mode Switching Key    : " + SWITCH_KEY)
        print("Setting Capture Area  : " + GRABZONE_KEY_UP + "/" + GRABZONE_KEY_DOWN)
        print("Bunny Hop Key         : " + BUNNY_KEY)
        print("==== Information ====")
        print("Mode                  : " + Fore.CYAN + mods[self.mode] + Style.RESET_ALL)
        print("Status                : " + (Fore.GREEN + "ON" if self.toggled else Fore.RED + "OFF") + Style.RESET_ALL)
        print("Bunny Hop             : " + (Fore.GREEN + "ON" if self._bunny else Fore.RED + "OFF") + Style.RESET_ALL)
        print("=====================")

    def start(self):
        init()
        self.print_banner()
        while True:
            if keyboard.is_pressed(TRIGGER_KEY):
                self.toggle()
                self.print_banner()
                time.sleep(0.3)
            if keyboard.is_pressed(SWITCH_KEY):
                self.switch()
                self.print_banner()
                time.sleep(0.3)
            if keyboard.is_pressed(BUNNY_KEY):
                self.bunny()
                self.print_banner()
                time.sleep(0.3)

            if self.toggled:
                try:
                    self.grab()
                except FoundEnemy:
                    current_time = time.time()
                    if current_time - self.last_reac > 0.1:
                        if self.mode == 0:
                            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
                            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up
                        elif self.mode == 1:
                            self.double_click()
                        elif self.mode == 2:
                            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
                            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up
                            self.double_click()
                        self.last_reac = current_time
                if self._bunny:
                    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
                    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up

            time.sleep(0.001)

tb = TriggerBot()
tb.start()
