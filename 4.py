import keyboard
import time
import ctypes
import os
import mss
from colorama import Fore, Style, init
from PIL import ImageGrab, Image
import winsound

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
ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

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
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
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
            sct_img = sct.grab(bbox)
            return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    def scan(self):
        start_time = time.time()
        pmap = self.grab()

        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if (
                        keyboard.is_pressed("w")
                        or keyboard.is_pressed("a")
                        or keyboard.is_pressed("s")
                        or keyboard.is_pressed("d")
                    ):
                        return  # Don't perform click if 'W', 'A', 'S', or 'D' is pressed
                    elif self.approx(r, g, b):
                        raise FoundEnemy
        except FoundEnemy:
            self.last_reac = int((time.time() - start_time) * 1000)
            self.double_click()
            if self.mode == 0:
                time.sleep(0.5)
            if self.mode == 1:
                time.sleep(0.25)
            if self.mode == 2:
                time.sleep(0.2)
            self.print_banner()

    def print_banner(self):
        os.system("cls")
        init()
        print(
            Fore.YELLOW
            + "Ousmane Valorant TriggerBot v1.0.0\n"
            + "===== Control =====\n"
            + "Activation key        : "
            + Fore.CYAN
            + TRIGGER_KEY
            + Style.RESET_ALL
            + "\n"
            + "Mode Switching Key    : "
            + Fore.CYAN
            + SWITCH_KEY
            + Style.RESET_ALL
            + "\n"
            + "Setting Capture Area  : "
            + Fore.CYAN
            + GRABZONE_KEY_UP
            + "/"
            + GRABZONE_KEY_DOWN
            + Style.RESET_ALL
            + "\n"
            + "==== Information ====\n"
            + "Mode                  : "
            + Fore.CYAN
            + mods[self.mode]
            + Style.RESET_ALL
            + "\n"
            + "Last Reaction Time    : "
            + Fore.CYAN
            + str(self.last_reac)
            + " ms"
            + Style.RESET_ALL
        )

    def start(self):
        self.print_banner()
        while True:
            if keyboard.is_pressed(TRIGGER_KEY):
                self.toggle()
                time.sleep(0.3)
                self.print_banner()
            if keyboard.is_pressed(SWITCH_KEY):
                self.switch()
                time.sleep(0.3)
                self.print_banner()
            if keyboard.is_pressed(BUNNY_KEY):
                self.bunny()
                time.sleep(0.3)
                self.print_banner()
            if self.toggled:
                self.scan()
            if self._bunny:
                ctypes.windll.user32.mouse_event(1, 0, 0, 120, 0)
                time.sleep(0.01)


if __name__ == "__main__":
    tb = TriggerBot()
    tb.start()
