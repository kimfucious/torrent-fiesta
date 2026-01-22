from enum import Enum

app_title = "Torrent Fiesta"
docker_compose_project_name = "torrent_fiesta"

app_root_on_disk = "/Volumes/Pteri/torrent_fiesta"
app_data_dir = f"{app_root_on_disk}/data"
app_media_dir = f"{app_data_dir}/media"

app_media_movies_dir = f"{app_media_dir}/movies"
app_media_tv_dir = f"{app_media_dir}/tv"
app_torrents_dir = f"{app_data_dir}/torrents"


class LogPath(Enum):
    PROWLARR = f"{app_root_on_disk}/prowlarr/config/logs/prowlarr.txt"
    RADARR = f"{app_root_on_disk}/radarr/config/logs/radarr.txt"
    SABNZBD = f"{app_root_on_disk}/sabnzbd/config/logs/sabnzbd.log"
    SONARR = f"{app_root_on_disk}/sonarr/config/logs/sonarr.txt"
    WHISPARR = f"{app_root_on_disk}/whisparr/config/logs/whisparr.txt"


class ServiceImageUrl(Enum):
    PROWLARR = "lscr.io/linuxserver/prowlarr:latest"
    RADARR = "lscr.io/linuxserver/radarr:latest"
    SABNZBD = "lscr.io/linuxserver/sabnzbd:latest" 
    SONARR = "lscr.io/linuxserver/sonarr:latest"
    WHISPARR = "ghcr.io/hotio/whisparr:v3"


class MediaPath(Enum):
    MEDIA = f"{app_media_dir}/"
    MOVIES = f"{app_media_movies_dir}/"
    TV = f"{app_media_tv_dir}/"


class MenuOption(Enum):
    BACK_TO_FULL_SERVICE = "Back to Full Service"
    BACK_TO_MAIN = "Back to Main Menu"

    FULL_SERVICE = "(F)ull Service"
    MOVIES = "(M)ovies"
    OPEN_PROWLARR = "Open (P)rowlarr"
    OPEN_RADARR = "Open (R)adarr"

    OPEN_SABNZBD = "Open SABN(Z)BD"
    OPEN_SONARR = "Open (S)onarr"
    OPEN_WHISPARR = "Open Whisparr"
    OPEN_MEDIA = "Open Media"
    OPEN_MEDIA_MOVIES = "Open Media/Movies"
    OPEN_MEDIA_TV = "Open Media/TV"

    PORN = "Porn"
    QUIT = "(Q)uit"
    RESTART_APP = "Res(t)art App"
    SHOW_LOGS = "Show (L)ogs"

    SWITCH_TO_FULL_SERVICE = "Switch to Full Service"
    SWITCH_TO_MOVIES = "Switch to Movies"
    SWITCH_TO_TV = "Switch to TV"
    TAIL_PROWLARR_LOG = "Tail Pro(w)larr Log"
    TAIL_RADARR_LOG = "Tail R(a)darr Log"

    TAIL_SONARR_LOG = "Tail S(o)narr Log"
    TAIL_SABNZBD_LOG = "Tail SAB(n)zbd Log"
    TAIL_WHISPARR_LOG = "Tail Whisparr Log"
    TV_SHOWS = "T(v) Shows"
    UPDATE_APPS = "(U)pdate Apps"
    UPDATE_PROWLARR = "Update Prowlarr"
    UPDATE_RADARR = "Update Radarr"
    UPDATE_SABNZBD = "Update SABnzbd"
    UPDATE_SONARR = "Update Sonarr"
    UPDATE_WHISPARR = "Update Whisparr"


class ComposeDirectory(Enum):
    FULL_SERVICE = "full_service"
    RADARR = "movies"
    SONARR = "tv"
    WHISPARR = "porn"


class FriendlyName(Enum):
    FULL_SERVICE = "Full Service"
    PROWLARR = "Prowlarr"
    RADARR = "Radarr"
    SONARR = "Sonarr"
    SABNZBD = "SABnzbd"
    WHISPARR = "Whisparr"


class ServiceName(Enum):
    FULL_SERVICE = "full_service"
    PROWLARR = "prowlarr"
    RADARR = "radarr"
    SONARR = "sonarr"
    SABNZBD = "sabnzbd"
    WHISPARR = "whisparr"


class ServiceUiUrl(Enum):
    PROWLARR = "http://localhost:9696"
    RADARR = "http://localhost:7878"
    SONARR = "http://localhost:8989"
    SABNZBD = "http://localhost:8080"
    WHISPARR = "http://localhost:6969"


class Service:
    def __init__(
            self,
            name,
            friendly_name,
            image_url,
            compose_dir=None,
            log_path=None,
            media_path=None,
            ui_url=None,
    ):
        self.name = name
        self.friendly_name = friendly_name
        self.image_url = image_url
        self.compose_dir = compose_dir
        self.ui_url = ui_url
        self.media_path = media_path
        self.log_path = log_path


class StateManager:
    def __init__(self):
        self.state = {'active_service': None}
        self.is_vpn = False

    prowlarr = Service(
        ServiceName.PROWLARR.value,
        FriendlyName.PROWLARR.value,
        ServiceImageUrl.PROWLARR.value,
        None,
        LogPath.PROWLARR,
        None,
        ServiceUiUrl.PROWLARR.value,
    )
    radarr = Service(
        ServiceName.RADARR.value,
        FriendlyName.RADARR.value,
        ServiceImageUrl.RADARR.value,
        ComposeDirectory.RADARR.value,
        LogPath.RADARR,
        MediaPath.MOVIES.value,
        ServiceUiUrl.RADARR.value,
    )

    sabnzbd = Service(
        ServiceName.SABNZBD.value,
        FriendlyName.SABNZBD.value,
        ServiceImageUrl.SABNZBD.value,
        None,
        LogPath.SABNZBD,
        MediaPath.MEDIA.value,
        ServiceUiUrl.SABNZBD.value,
    )
    sonarr = Service(
        ServiceName.SONARR.value,
        FriendlyName.SONARR.value,
        ServiceImageUrl.SONARR.value,
        ComposeDirectory.SONARR.value,
        LogPath.SONARR,
        MediaPath.TV.value,
        ServiceUiUrl.SONARR.value,
    )
    whisparr = Service(
        ServiceName.WHISPARR.value,
        FriendlyName.WHISPARR.value,
        ServiceImageUrl.WHISPARR.value,
        ComposeDirectory.WHISPARR.value,
        LogPath.WHISPARR,
        MediaPath.MEDIA.value,
        ServiceUiUrl.WHISPARR.value,
    )
    full_service = Service(
        ServiceName.FULL_SERVICE.value,
        FriendlyName.FULL_SERVICE.value,
        None,
        ComposeDirectory.FULL_SERVICE.value,
        None,
        MediaPath.MEDIA.value,
        None
    )

    def set_state(self, key, value):
        self.state[key] = value

    def get_state(self, key):
        return self.state.get(key)

    def set_active_service(self, service):
        self.state["active_service"] = service

    def get_active_service(self):
        return self.state["active_service"]

    def set_is_vpn(self, is_vpn: bool):
        self.state["is_vpn"] = is_vpn

    def get_is_vpn(self):
        return self.state["is_vpn"]
