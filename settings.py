import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


DEFAULT_TF_ROOT = "/Volumes/Pteri/torrent_fiesta"
DEFAULT_TF_TZ = "UTC"
DEFAULT_TF_BROWSER_MODE = "default"
DEFAULT_TF_ENABLE_UI_CLOSE = "true"
DEFAULT_TF_TRANSMISSION_MODE = "auto"



def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default



def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class RuntimeSettings:
    tf_root: str
    tf_tz: str
    tf_browser_mode: str
    tf_enable_ui_close: bool
    tf_transmission_mode: str
    tf_transmission_exe: Optional[str]



def load_settings() -> RuntimeSettings:
    _load_dotenv(Path(".env"))

    default_browser_mode = "default" if os.name == "nt" else "chrome"
    browser_mode = os.getenv("TF_BROWSER_MODE", default_browser_mode).strip().lower()
    if browser_mode not in {"default", "chrome"}:
        browser_mode = default_browser_mode

    transmission_mode = os.getenv(
        "TF_TRANSMISSION_MODE", DEFAULT_TF_TRANSMISSION_MODE
    ).strip().lower()
    if transmission_mode not in {"auto", "manual"}:
        transmission_mode = DEFAULT_TF_TRANSMISSION_MODE

    return RuntimeSettings(
        tf_root=os.getenv("TF_ROOT", DEFAULT_TF_ROOT).strip(),
        tf_tz=os.getenv("TF_TZ", DEFAULT_TF_TZ).strip(),
        tf_browser_mode=browser_mode,
        tf_enable_ui_close=_to_bool(
            os.getenv("TF_ENABLE_UI_CLOSE", DEFAULT_TF_ENABLE_UI_CLOSE), default=True
        ),
        tf_transmission_mode=transmission_mode,
        tf_transmission_exe=os.getenv("TF_TRANSMISSION_EXE", "").strip() or None,
    )


SETTINGS = load_settings()


def docker_runtime_env() -> dict:
    env = os.environ.copy()
    env.setdefault("TF_ROOT", SETTINGS.tf_root)
    env.setdefault("TF_TZ", SETTINGS.tf_tz)
    env.setdefault("TF_PUID", env.get("TF_PUID", "1000"))
    env.setdefault("TF_PGID", env.get("TF_PGID", "1000"))
    return env
