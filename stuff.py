from globals import docker_compose_project_name, Service, ServiceName
from halo import Halo
from platform_adapter import (
    clear_screen,
    close_service_ui_tabs,
    is_process_running,
    open_url,
    start_application,
    follow_file,
    wait_for_process,
)
from settings import SETTINGS, docker_runtime_env
from termcolor import colored
import subprocess
import time


def is_docker_running():
    result = subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0



def is_transmission_running():
    return (
        is_process_running("transmission")
        or is_process_running("transmission-qt")
        or is_process_running("Transmission")
    )



def start_docker():
    launch_attempted = False

    while True:
        if is_docker_running():
            return

        clear_screen()
        print(colored("Docker Desktop is not running.", "red"))

        if not launch_attempted and start_application("docker"):
            print("Attempting to start Docker Desktop...")
            launch_attempted = True
            time.sleep(3)
            continue

        print("\nPlease start Docker Desktop manually to continue, or press 'q' to quit.")
        choice = input("\n[r] Retry check | [q] Quit: ").lower().strip()

        if choice == "q":
            from helpers import quit_app

            quit_app()



def _prompt_transmission_retry() -> str:
    print(colored("\nTransmission is not running.", "yellow"))
    print("Start it manually, or let Torrent Fiesta try again.")
    return input("\n[r] Retry | [c] Continue anyway | [q] Quit: ").lower().strip()



def start_transmission():
    if is_transmission_running():
        return

    mode = SETTINGS.tf_transmission_mode

    while True:
        started = False
        if mode == "auto":
            spinner = Halo(text="Starting Transmission...", spinner="dots")
            spinner.start()
            started = start_application("transmission")
            if started and wait_for_process("transmission", timeout_seconds=15):
                spinner.succeed("Transmission started successfully!")
                return
            spinner.fail("Could not auto-start Transmission.")

        choice = _prompt_transmission_retry()
        if choice == "q":
            from helpers import quit_app

            quit_app()
        elif choice == "c":
            print(colored("Continuing without Transmission auto-check.", "cyan"))
            return
        elif choice == "r":
            if is_transmission_running():
                return
            if mode != "auto":
                continue
            if not started:
                continue



def open_ui(service: Service = None):
    if service is None or service.ui_url is None:
        return
    open_url(service.ui_url)



def close_ui(service_name: str):
    if service_name is None:
        return
    close_service_ui_tabs(service_name)



def get_running_docker_compose_projects():
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Label \"com.docker.compose.project\"}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    compose_projects = result.stdout.strip().split("\n") if result.stdout.strip() else []
    unique_projects = list(set(compose_projects))
    return unique_projects



def stop_docker_compose(service: Service):
    if service is None:
        return

    project = docker_compose_project_name
    name = service.friendly_name

    try:
        subprocess.run(
            ["docker", "compose", "-p", project, "ps"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=docker_runtime_env(),
        )
    except subprocess.CalledProcessError:
        return

    print(" ")
    spinner = Halo(text=f"Stopping {name}...", spinner="dots")
    spinner.start()
    subprocess.run(
        ["docker", "compose", "-p", project, "down"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        env=docker_runtime_env(),
    )
    spinner.stop()



def tail_log(path):
    print(colored("\nPress Ctrl+C to exit logging", "cyan"))
    try:
        follow_file(path, lines=25)
    except KeyboardInterrupt:
        print("\nExiting logging mode.")



def wait():
    from helpers import wait_for_keypress

    print(colored("Press any key to continue", "cyan"))
    wait_for_keypress()



def start_service(service: Service):
    label = service.friendly_name
    compose_project_name = docker_compose_project_name
    compose_dir = service.compose_dir

    if not compose_dir:
        return

    path = f"docker/services/{compose_dir}/compose.yaml"
    spinner = Halo(text=f"Starting {label}...", spinner="dots")
    spinner.start()

    process = subprocess.run(
        [
            "docker",
            "compose",
            "-p",
            compose_project_name,
            "-f",
            path,
            "up",
            "-d",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        env=docker_runtime_env(),
    )

    if process.returncode != 0:
        stderr = process.stderr.strip()
        if "Conflict" in stderr:
            spinner.fail("Something is already running. Restarting...")
            stop_docker_compose(service)
            start_service(service)
            return

        spinner.fail(f"Error starting {service.name}.")
        if stderr:
            print(f"\n{stderr}\n")
        input("Press Enter to continue...")
        return

    if service.ui_url:
        time.sleep(2)
        open_ui(service)

    spinner.succeed()



def stop_service(service: Service = None):
    stop_docker_compose(service)
    if service is None:
        return

    service_name = service.name
    if service_name == ServiceName.FULL_SERVICE.value:
        close_ui(ServiceName.PROWLARR.value)
        close_ui(ServiceName.RADARR.value)
        close_ui(ServiceName.SABNZBD.value)
        close_ui(ServiceName.SONARR.value)
        close_ui(ServiceName.WHISPARR.value)
        return

    close_ui(ServiceName.PROWLARR.value)
    close_ui(service_name)



def update_service(service: Service = None):
    service_name = service.name
    if service_name is None:
        print("Service Not Configured for Update")
        time.sleep(3)
        return

    image = service.image_url
    print(" ")

    spinner = Halo(text=f"Updating {service.friendly_name}...", spinner="dots")
    spinner.start()

    process = subprocess.run(["docker", "pull", image], check=False)
    if process.returncode == 0:
        spinner.succeed()
        return

    spinner.fail("Error updating service.")
