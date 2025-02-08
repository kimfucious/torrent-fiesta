from globals import (docker_compose_project_name, Service, ServiceName)
from halo import Halo
from termcolor import colored
import os
import shlex
import subprocess
import time


def is_docker_running():
    result = subprocess.run(shlex.split("pgrep Docker"),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0


def is_transmission_running():
    result = subprocess.run(shlex.split("pgrep Transmission"),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0


def start_docker():
    if not is_docker_running():
        spinner = Halo(text="Starting Docker...", spinner="dots")
        spinner.start()
        subprocess.run(shlex.split('open -a "Docker"'))
        # Wait until Docker is running
        while not is_docker_running():
            continue
        spinner.succeed("Docker started successfully!")


def start_transmission():
    if not is_transmission_running():
        spinner = Halo(text="Starting Transmission...", spinner="dots")
        spinner.start()
        subprocess.run(shlex.split('open -a "Transmission"'))
        # Wait until Transmission is running
        while not is_transmission_running():
            continue
        spinner.succeed("Transmission started successfully!")


def open_ui(service: Service = None):
    if service is None or service.ui_url is None:
        return
    path = service.ui_url
    subprocess.run(shlex.split(
        f'open -a "Google Chrome" {path}'))


def close_ui(service_name: str):
    if service_name is None:
        return

    name = service_name

    # Check if the tab exists before attempting to close it
    check_command = shlex.split(
        f"osascript -e 'tell application \"Google Chrome\""
        f" to exists (tab of window 1 whose title contains \"{name}\")'"
    )
    check_result = subprocess.run(
        check_command, capture_output=True, text=True)

    if check_result.stdout.strip() == "true":
        close_command = shlex.split(
            f"osascript -e 'tell application \"Google Chrome\""
            f" to close (tabs of window 1 whose title contains \"{name}\")'"
        )
        subprocess.run(close_command)
    else:
        return


def get_running_docker_compose_projects():
    cmd = 'docker ps --format "{{.Label \\"com.docker.compose.project\\"}}"'
    args = shlex.split(cmd)
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    compose_projects = result.stdout.strip().split("\n")
    unique_projects = list(set(compose_projects))

    return unique_projects


def stop_docker_compose(service: Service):
    try:
        if service is None:
            return
        project = docker_compose_project_name
        name = service.friendly_name
        # Suppress output by redirecting stdout and stderr to DEVNULL
        with open(os.devnull, 'w') as devnull:
            subprocess.run(shlex.split(
                f'docker compose -p {project} ps'),
                check=True,
                stdout=devnull,
                stderr=subprocess.DEVNULL)
            print(" ")
            spinner = Halo(text=f"Stopping {name}...", spinner="dots")
            spinner.start()
            subprocess.run(shlex.split(
                f'docker compose -p {project} down'),
                stdout=devnull,
                stderr=subprocess.DEVNULL)
            spinner.stop()
    except subprocess.CalledProcessError:
        return


def tail_log(path):
    print(colored("\nPress Ctrl+C to exit logging", "cyan"))
    try:
        subprocess.run(shlex.split(f'tail -n 25 -f {path}'), check=True)
    except KeyboardInterrupt:
        print("\nExiting logging mode.")


# def is_compose_up(project: str) -> bool:
#     # Use Docker CLI or Docker SDK to check if containers are running
#     # Return True if containers are running, False otherwise
#     # Example using Docker CLI:
#     try:
#         output = subprocess.check_output(
#             ['docker', 'ps', '--filter', f'name={project}',
#              '--format', '{{.ID}}'])
#         return bool(output)
#     except subprocess.CalledProcessError:
#         return False

def wait():
    from helpers import wait_for_keypress
    print(colored("Press any key to continue", "cyan"))
    wait_for_keypress()


def start_service(service: Service):
    label = service.friendly_name
    compose_project_name = docker_compose_project_name
    # service_name = service.name
    compose_dir = service.compose_dir
    try:
        path = f"docker/services/{compose_dir}/compose.yaml"
        # print("name", service_name)
        # print("project", compose_project_name)
        # print("path", path)
        # wait()
        spinner = Halo(text=f"Starting {label}...", spinner="dots")
        spinner.start()
        process = subprocess.run(
            shlex.split(
                f'docker compose -p {compose_project_name} -f {path} up -d'
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensure the output is returned as a string
        )

        # Use this for debug
        # subprocess.run(
        #     shlex.split(
        #         f'docker compose -p {compose_project_name} -f {path} up'
        #     ),
        # )

    except subprocess.CalledProcessError as e:
        if "Conflict" in str(e):
            # Handle conflict error
            spinner.fail("Something is already running.  Restarting...")
            stop_docker_compose(service)
            start_service(service)
        else:
            print(f"Error starting {service.name}: {e}")
            time.sleep(10)
        return

    # Check for any output (stdout or stderr) and print it if needed
    # Comment out for debug
    output = process.stdout.strip()
    if output:
        print(output)

    # Service started successfully, continue with other operations
    if service.ui_url:
        time.sleep(2)
        open_ui(service)
    spinner.succeed()


# def start_service2(service: Service):
#     label = service.friendly_name
#     name = docker_compose_project_name
#     project = service.compose_project_filename
#     try:
#         path = f"docker/{project}-compose.yaml"
#         spinner = Halo(text=f"Starting {label}...", spinner="dots")
#         spinner.start()
#         with open("docker_up.log", "w") as log_file:
#             subprocess.run(
#                 shlex.split(
#                     f'docker compose -p {name} -f {path} up -d'
#                 ),
#                 stdout=log_file,
#                 stderr=subprocess.STDOUT  # Redirect stderr to stdout
#             )

#     except subprocess.CalledProcessError as e:
#         if "Conflict" in str(e):
#             # Handle conflict error
#             spinner.fail("Something is already running.  Restarting...")
#             stop_docker_compose(service)
#             start_service(service)
#         else:
#             print(f"Error starting {service.name}: {e}")
#         return

#     # Service started successfully, continue with other operations
#     time.sleep(2)
#     open_ui(service)
#     spinner.stop()


# def start_service3(service: Service):
#     name = docker_compose_project_name
#     project = service.compose_project_filename
#     try:
#         path = f"docker/{project}-compose.yaml"
#         spinner = Halo(text=f"Starting {project} ...", spinner="dots")
#         spinner.start()
#         subprocess.run(shlex.split(
#             f'docker compose -p {name} -f {path} up -d'))

#     except subprocess.CalledProcessError as e:
#         if "Conflict" in str(e):
#             # spinner.fail("Something is already running.  Restarting...")
#             stop_docker_compose(service)
#             start_service(service)
#         else:
#             print(f"Error starting {service.name}: {e}")
#         return

#     time.sleep(2)
#     # spinner.stop()
#     open_ui(service)


def stop_service(service: Service = None):
    stop_docker_compose(service)
    if (service is None):
        return
    service_name = service.name
    if service_name == ServiceName.FULL_SERVICE.value:
        close_ui(ServiceName.PROWLARR.value)
        close_ui(ServiceName.RADARR.value)
        close_ui(ServiceName.READARR.value)
        close_ui(ServiceName.SABNZBD.value)
        close_ui(ServiceName.SONARR.value)
        close_ui(ServiceName.WHISPARR.value)
        return
    else:
        close_ui(ServiceName.PROWLARR.value)
        close_ui(service_name)
        return


def stop_docker():
    # This doesn't work!
    applescript = '''
    tell application "Docker"
        quit
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])


def update_service(service: Service = None):
    # This menu option is only available through main menu
    # Services are not running at this point
    service_name = service.name
    if service_name is None:
        print("Service Not Configured for Update")
        time.sleep(3)
        return
    image = service.image_url
    print(" ")
    try:
        spinner = Halo(text=f"Updating {
                       service.friendly_name}...", spinner="dots")
        spinner.start()
        subprocess.run(["docker", "pull", image])
        spinner.succeed()
        return
    except subprocess.CalledProcessError as e:
        spinner.fail("Error updating service.", e)
        return
