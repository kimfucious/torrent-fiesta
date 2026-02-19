from art import text2art
from halo import Halo
from globals import (Service, ServiceName)
from stuff import (close_ui, stop_docker_compose)
from platform_adapter import clear_screen as platform_clear_screen
from platform_adapter import open_folder
from termcolor import colored
import os
import random
import sys
import time


def clear_screen():
    platform_clear_screen()
    return


def get_color():
    colors = ["cyan", "magenta", "yellow", "green", "blue", "red"]
    return random.choice(colors)


def open_location(service: Service):
    if service is None or service.media_path is None:
        return

    open_folder(service.media_path)


def print_ascii_art(text, color):
    art_1 = text2art(f"{text}", font="small")
    print(colored(art_1, color))


def restart_app(service: Service):
    if service is not None:
        stop_docker_compose(service)
    spinner = Halo(text="Restarting App...", spinner="dots")
    spinner.start()
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)


def quit_app():
    close_ui(ServiceName.PROWLARR.value)
    clear_screen()
    print(colored("\n🌺 Aloha!", "green"))
    exit()


def wait_for_keypress():
    try:
        # Attempt to use msvcrt for Windows
        import msvcrt

        _ = msvcrt.getch()
    except ImportError:
        # Fall back to tty for Unix-based systems
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            _ = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
