from globals import (
    app_title,
    LogPath,
    MenuOption,
    Service,
    ServiceName,
    StateManager
)

from helpers import (
    clear_screen,
    open_location,
    print_ascii_art,
    restart_app,
    quit_app,
    wait_for_keypress,
)

from stuff import (
    open_ui,
    start_service,
    stop_service,
    tail_log,
    update_service
)

from typing import Union

from termcolor import colored

alpha_menu_options = {
    "a": MenuOption.TAIL_RADARR_LOG.value,
    "b": MenuOption.BOOKS.value,
    "d": MenuOption.OPEN_READARR.value,
    "e": MenuOption.TAIL_READARR_LOG.value,
    "f": MenuOption.FULL_SERVICE.value,
    "l": MenuOption.SHOW_LOGS.value,
    "m": MenuOption.MOVIES.value,
    "n": MenuOption.TAIL_SABNZBD_LOG.value,
    "o": MenuOption.TAIL_SONARR_LOG.value,
    "p": MenuOption.OPEN_PROWLARR.value,
    "q": MenuOption.QUIT.value,
    "r": MenuOption.OPEN_RADARR.value,
    "s": MenuOption.OPEN_SONARR.value,
    "t": MenuOption.RESTART_APP.value,
    "u": MenuOption.UPDATE_APPS.value,
    "v": MenuOption.TV_SHOWS.value,
    "w": MenuOption.TAIL_PROWLARR_LOG.value,
    "z": MenuOption.OPEN_SABNZBD.value,
}

main_menu_options = {
    1: MenuOption.BOOKS.value,
    2: MenuOption.MOVIES.value,
    3: MenuOption.TV_SHOWS.value,
    4: MenuOption.FULL_SERVICE.value,
    5: MenuOption.RESTART_APP.value,
    6: MenuOption.UPDATE_APPS.value,
    7: MenuOption.QUIT.value,
}

full_service_options = {
    1: MenuOption.OPEN_PROWLARR.value,
    2: MenuOption.OPEN_SABNZBD.value,
    3: MenuOption.OPEN_RADARR.value,
    4: MenuOption.OPEN_READARR.value,
    5: MenuOption.OPEN_SONARR.value,
    6: MenuOption.OPEN_MEDIA.value,
    7: MenuOption.SHOW_LOGS.value,
    8: MenuOption.RESTART_APP.value,
    9: MenuOption.QUIT.value,
}

log_menu_options = {
    1: MenuOption.TAIL_PROWLARR_LOG.value,
    2: MenuOption.TAIL_RADARR_LOG.value,
    3: MenuOption.TAIL_READARR_LOG.value,
    4: MenuOption.TAIL_SABNZBD_LOG.value,
    5: MenuOption.TAIL_SONARR_LOG.value,
    6: MenuOption.BACK_TO_FULL_SERVICE.value,
}

books_menu_options = {
    1: MenuOption.OPEN_PROWLARR.value,
    2: MenuOption.OPEN_READARR.value,
    3: MenuOption.SWITCH_TO_MOVIES.value,
    4: MenuOption.SWITCH_TO_TV.value,
    5: MenuOption.SWITCH_TO_FULL_SERVICE.value,
    6: MenuOption.TAIL_READARR_LOG.value,
    7: MenuOption.UPDATE_READARR.value,
    8: MenuOption.QUIT.value,
}

movie_menu_options = {
    1: MenuOption.OPEN_PROWLARR.value,
    2: MenuOption.OPEN_RADARR.value,
    3: MenuOption.SWITCH_TO_BOOKS.value,
    4: MenuOption.SWITCH_TO_TV.value,
    5: MenuOption.SWITCH_TO_FULL_SERVICE.value,
    6: MenuOption.TAIL_RADARR_LOG.value,
    7: MenuOption.QUIT.value,
}

tv_menu_options = {
    1: MenuOption.OPEN_PROWLARR.value,
    2: MenuOption.OPEN_SONARR.value,
    3: MenuOption.SWITCH_TO_BOOKS.value,
    4: MenuOption.SWITCH_TO_MOVIES.value,
    5: MenuOption.SWITCH_TO_FULL_SERVICE.value,
    6: MenuOption.TAIL_SONARR_LOG.value,
    7: MenuOption.QUIT.value,
}

update_menu_options = {
    1: MenuOption.UPDATE_PROWLARR.value,
    2: MenuOption.UPDATE_RADARR.value,
    3: MenuOption.UPDATE_READARR.value,
    4: MenuOption.UPDATE_SONAR.value,
    5: MenuOption.BACK_TO_MAIN.value,
}


def init_menu(state_manager):
    clear_screen()
    run_main_menu(state_manager)


def get_title(service: Service = None):
    if (service is None):
        return f"{app_title}"

    name = service.name
    if name == ServiceName.RADARR.value:
        return f"{app_title} Movies"
    elif name == ServiceName.READARR.value:
        return f"{app_title} Books"
    elif name == ServiceName.SONARR.value:
        return f"{app_title} TV"
    elif name == ServiceName.FULL_SERVICE.value:
        return f"{app_title} Full Service"
    else:
        return f"{app_title}"


def print_menu(options, state_manager: StateManager):
    active_service: Service = state_manager.get_active_service()
    title = get_title(active_service)
    color = get_color_for_service(active_service)
    clear_screen()
    print_ascii_art(title, color)
    for key in options.keys():
        print(f"{key}. {options[key]}")


def get_color_for_service(service: Service = None):
    if (service is None):
        return "red"

    name = service.name
    if name == ServiceName.RADARR.value:
        return "yellow"
    elif name == ServiceName.READARR.value:
        return "magenta"
    elif name == ServiceName.SONARR.value:
        return "cyan"
    else:
        return "red"


def handle_option(options, selection, state_manager: StateManager):
    selected_option = options[selection]
    active_service: Union[Service,  None] = state_manager.get_active_service()
    if selected_option == MenuOption.BACK_TO_FULL_SERVICE.value:
        state_manager.set_active_service(state_manager.full_service)
        run_full_service(state_manager)
    elif selected_option == MenuOption.BACK_TO_MAIN.value:
        run_main_menu(state_manager)
    elif selected_option == MenuOption.BOOKS.value:
        state_manager.set_active_service(state_manager.readarr)
        start_service(state_manager.readarr)
        run_books_menu(state_manager)
    elif selected_option == MenuOption.SWITCH_TO_BOOKS.value:
        if (active_service is not None):
            stop_service(active_service)
        state_manager.set_active_service(state_manager.readarr)
        start_service(state_manager.readarr)
        run_books_menu(state_manager)
    elif selected_option == MenuOption.MOVIES.value:
        state_manager.set_active_service(state_manager.radarr)
        start_service(state_manager.radarr)
        run_movies_menu(state_manager)
    elif selected_option == MenuOption.SWITCH_TO_MOVIES.value:
        if (active_service is not None):
            stop_service(active_service)
        state_manager.set_active_service(state_manager.radarr)
        start_service(state_manager.radarr)
        run_movies_menu(state_manager)
    elif selected_option == MenuOption.TV_SHOWS.value:
        state_manager.set_active_service(state_manager.sonarr)
        start_service(state_manager.sonarr)
        run_tv_menu(state_manager)
    elif selected_option == MenuOption.SWITCH_TO_TV.value:
        if (active_service is not None):
            stop_service(active_service)
        state_manager.set_active_service(state_manager.sonarr)
        start_service(state_manager.sonarr)
        run_tv_menu(state_manager)
    elif selected_option == MenuOption.FULL_SERVICE.value:
        start_service(state_manager.full_service)
        state_manager.set_active_service(state_manager.full_service)
        run_full_service(state_manager)
    elif selected_option == MenuOption.SWITCH_TO_FULL_SERVICE.value:
        if (active_service is not None):
            stop_service(active_service)
        state_manager.set_active_service(state_manager.full_service)
        start_service(state_manager.full_service)
        run_full_service(state_manager)
    elif selected_option == MenuOption.OPEN_MEDIA.value:
        if (active_service is not None):
            open_location(active_service)
    elif selected_option == MenuOption.OPEN_PROWLARR.value:
        open_ui(state_manager.prowlarr)
    elif selected_option == MenuOption.OPEN_RADARR.value:
        open_ui(state_manager.radarr)
    elif selected_option == MenuOption.OPEN_READARR.value:
        open_ui(state_manager.readarr)
    elif selected_option == MenuOption.OPEN_SABNZBD.value:
        open_ui(state_manager.sabnzbd)
    elif selected_option == MenuOption.OPEN_SONARR.value:
        open_ui(state_manager.sonarr)
    elif selected_option == MenuOption.RESTART_APP.value:
        choice = input(
            colored("\nAre you sure you want to restart? (y/n): ", "red"))
        if choice.isalpha() and choice.lower() == "y":
            restart_app(active_service)
        else:
            if active_service is not None and active_service.name == \
                    ServiceName.FULL_SERVICE.value:
                run_full_service(state_manager)
            else:
                run_main_menu(state_manager)
    elif selected_option == MenuOption.SHOW_LOGS.value:
        run_logs_menu(state_manager)
    elif selected_option == MenuOption.TAIL_PROWLARR_LOG.value:
        tail_log(LogPath.PROWLARR.value)
    elif selected_option == MenuOption.TAIL_RADARR_LOG.value:
        tail_log(LogPath.RADARR.value)
    elif selected_option == MenuOption.TAIL_READARR_LOG.value:
        tail_log(LogPath.READARR.value)
    elif selected_option == MenuOption.TAIL_SABNZBD_LOG.value:
        tail_log(LogPath.SABNZBD.value)
    elif selected_option == MenuOption.TAIL_SONARR_LOG.value:
        tail_log(LogPath.SONARR.value)
    elif selected_option == MenuOption.UPDATE_APPS.value:
        run_update_menu(state_manager)
    elif selected_option == MenuOption.UPDATE_PROWLARR.value:
        update_service(state_manager.prowlarr)
    elif selected_option == MenuOption.UPDATE_RADARR.value:
        update_service(state_manager.radarr)
    elif selected_option == MenuOption.UPDATE_READARR.value:
        update_service(state_manager.readarr)
    elif selected_option == MenuOption.UPDATE_SONARR.value:
        update_service(state_manager.sonarr)
    elif selected_option == MenuOption.QUIT.value:
        stop_service(active_service)
        quit_app()


def run_menu(options, handler, state_manager):
    while True:
        print_menu(options, state_manager)
        try:
            choice = input("\nEnter selection: ")
            if choice.isdigit():
                choice = int(choice)
                if choice in options:
                    handler(options, choice, state_manager)
                else:
                    clear_screen()
            elif choice.isalpha():
                if choice in alpha_menu_options:
                    handler(alpha_menu_options, choice, state_manager)
                else:
                    clear_screen()
            else:
                clear_screen()
        except ValueError as e:
            print("Error", e)
            print(colored("\nPlease select a valid menu option.", "yellow"))
            print(colored("\nPress any key to continue", "cyan"))
            wait_for_keypress()
            clear_screen()


def run_full_service(state_manager):
    run_menu(full_service_options, handle_option, state_manager)


def run_books_menu(state_manager):
    run_menu(books_menu_options, handle_option, state_manager)


def run_movies_menu(state_manager):
    run_menu(movie_menu_options, handle_option, state_manager)


def run_tv_menu(state_manager):
    run_menu(tv_menu_options, handle_option, state_manager)


def run_logs_menu(state_manager):
    run_menu(log_menu_options, handle_option, state_manager)


def run_update_menu(state_manager):
    run_menu(update_menu_options, handle_option, state_manager)


def run_main_menu(state_manager):
    run_menu(main_menu_options, handle_option, state_manager)
