from menu import init_menu
from stuff import (start_docker, start_transmission)
from helpers import (
    clear_screen,
    print_ascii_art
)
from globals import (app_title, StateManager)

state_manager = StateManager()

if __name__ == '__main__':
    clear_screen()
    print_ascii_art(app_title, "red")
    start_docker()
    start_transmission()
    init_menu(state_manager)
