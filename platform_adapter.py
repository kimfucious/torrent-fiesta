import os
import subprocess
import time
import webbrowser
from pathlib import Path

from settings import SETTINGS


_WARNED = set()



def _warn_once(key: str, message: str) -> None:
    if key in _WARNED:
        return
    print(message)
    _WARNED.add(key)



def is_windows() -> bool:
    return os.name == "nt"



def clear_screen() -> None:
    os.system("cls" if is_windows() else "clear")



def open_url(url: str) -> None:
    if not url:
        return

    if is_windows() and SETTINGS.tf_browser_mode == "chrome":
        chrome_candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for candidate in chrome_candidates:
            if Path(candidate).exists():
                subprocess.run([candidate, url], check=False)
                return

    if not is_windows() and SETTINGS.tf_browser_mode == "chrome":
        subprocess.run(["open", "-a", "Google Chrome", url], check=False)
        return

    webbrowser.open(url)



def open_folder(path: str) -> bool:
    if not path:
        _warn_once("missing_path", "No folder path configured.")
        return False

    normalized = os.path.normpath(path)
    if not os.path.exists(normalized):
        _warn_once(
            f"folder_missing:{normalized}",
            f"Path does not exist: {normalized}",
        )
        return False

    if is_windows():
        subprocess.run(["explorer", normalized], check=False)
        return True

    subprocess.run(["open", "-a", "Finder", normalized], check=False)
    subprocess.run(["osascript", "-e", 'tell application "Finder" to activate'], check=False)
    return True



def is_process_running(process_hint: str) -> bool:
    if not process_hint:
        return False

    if is_windows():
        result = subprocess.run(
            ["tasklist"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return False
        return process_hint.lower() in result.stdout.lower()

    result = subprocess.run(
        ["pgrep", "-f", process_hint],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.returncode == 0



def _start_windows_executable(executable: str) -> bool:
    if not executable:
        return False

    exe_path = Path(executable)
    if not exe_path.exists():
        return False

    os.startfile(str(exe_path))
    return True



def start_application(app_id: str) -> bool:
    if not app_id:
        return False

    app_key = app_id.strip().lower()

    if is_windows():
        if app_key == "docker":
            return _start_windows_executable(r"C:\Program Files\Docker\Docker\Docker Desktop.exe")

        if app_key == "transmission":
            if SETTINGS.tf_transmission_exe and _start_windows_executable(SETTINGS.tf_transmission_exe):
                return True

            known_candidates = [
                r"C:\Program Files\Transmission\transmission-qt.exe",
                r"C:\Program Files (x86)\Transmission\transmission-qt.exe",
            ]
            for candidate in known_candidates:
                if _start_windows_executable(candidate):
                    return True
            return False

        return False

    app_map = {
        "docker": "Docker",
        "transmission": "Transmission",
    }
    app_name = app_map.get(app_key)
    if not app_name:
        return False

    subprocess.run(["open", "-a", app_name], check=False)
    return True



def close_service_ui_tabs(service_name: str) -> bool:
    if not service_name or not SETTINGS.tf_enable_ui_close:
        return False

    if is_windows():
        if SETTINGS.tf_browser_mode != "chrome":
            _warn_once(
                "ui_close_disabled_windows",
                "UI tab close automation is disabled on Windows when TF_BROWSER_MODE is not 'chrome'.",
            )
            return False

        if not is_process_running("chrome.exe"):
            return False

        _warn_once(
            "ui_close_not_supported_windows",
            "Chrome tab close automation is not reliable on Windows here; leaving tabs open.",
        )
        return False

    if SETTINGS.tf_browser_mode != "chrome":
        return False

    check_cmd = [
        "osascript",
        "-e",
        (
            "tell application \"Google Chrome\" "
            f"to exists (tab of window 1 whose title contains \"{service_name}\")"
        ),
    ]
    check_result = subprocess.run(
        check_cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    if check_result.stdout.strip().lower() != "true":
        return False

    close_cmd = [
        "osascript",
        "-e",
        (
            "tell application \"Google Chrome\" "
            f"to close (tabs of window 1 whose title contains \"{service_name}\")"
        ),
    ]
    subprocess.run(close_cmd, check=False)
    return True



def follow_file(path: str, lines: int = 25) -> None:
    if is_windows():
        command = (
            f'Get-Content -LiteralPath "{path}" -Tail {lines} -Wait'
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            check=False,
        )
        return

    subprocess.run(["tail", "-n", str(lines), "-f", path], check=True)



def wait_for_process(process_hint: str, timeout_seconds: int = 15) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if is_process_running(process_hint):
            return True
        time.sleep(1)
    return False
