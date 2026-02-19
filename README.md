# Torrent Fiesta 🎉

This is a project to simplify running [Servarr](https://wiki.servarr.com/) apps in Docker containers.

This project runs on macOS and Windows with Docker Desktop.
Windows support is for native Python on Windows (PowerShell/CMD), not WSL.

At present, [Lidarr](https://wiki.servarr.com/en/lidarr) and [Whisparr](https://wiki.servarr.com/en/whisparr) are not implemented.

Python is used to provide a CLI for running the app and performing various tasks like launching apps (e.g. Docker & Transmission), opening Servarr apps in browser tabs, and upping/downing Docker compose projects.

[Prowler](https://prowlarr.com/) is used to manage indexers here, but [Jackett](https://github.com/Jackett/Jackett) could be easily swapped in.

While this project could be taken further to integrate with a media server (e.g. [Plex](https://www.plex.tv/)), that has not been done or documented (yet).

This project assumes the use of [Transmission](https://transmissionbt.com/) as a Bittorrent client, but using something else should not be that hard to do.

Same goes for SABnzbd[https://sabnzbd.org/], which this project uses as a Usenet newsreader.

**!!! WARNING !!!:** Encapsulation of network traffic with a VPN is not implemented (yet), running this project without a pushing your Bittorrent and UseNet traffic through a VPN will probably get you into trouble with your ISP and possibly other entities in most countries.

## Prerequisites

-   Read the [documentation](#documentation).
-   The information found in [Helpful Links](#helpful-links) can be useful as well, esp. if you get stuck.

### Docker

-   If not already installed, install [Docker Desktop](https://docs.docker.com/desktop/).

Docker is used to run the Servarr and SABnzbd apps in containers. The Compose files are located in the docker directory at the root level of this project.

The app will select the correct files to use to run compose up/down commands based on CLI Menu selections.

You can run Servarr apps individually or select `Full Service` to run them all at once.

If you don't want a specific Servarr app to run in Full Service, edit the `/docker/services/full_service/compose.yaml` file, commenting out or deleting the service(s) you do not wish to use.  You'll need to edit the `full_service_options` dictionary in `menu.py` to remove services from the [CLI Menu](#the-cli-menu).

### Python

-   Install Python 3 and pip.
-   In terminal, navigate to the root of this project and run the following commands to install dependencies in an isolated environment.

```console
> python3 -m venv .venv
> source .venv/bin/activate
> python3 -m pip install -r requirements.txt
```

**NOTE:** The `.venv` directory and its subdirectories are excluded in `.gitignore`.

Windows PowerShell equivalent:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Folder Structure

This is one of the more confusing things when getting started.  

- Apps rely on `Download Clients` (e.g. Bittorrent/Transmission, Usenet/SABnzbs) to download files.
- Download Clients can be configured to place in-progress (i.e. incomplete) downloads in a particular directory.  
    - For Transmission this is done in the Transmission app under Settings => Transfers => Adding => Keep incomplete file in.  Servarr apps don't much care about this setting, so it's not super important where this is. 

Create a folder structure like this on your local machine:

```shell
.
├── data
│   ├── media # Servarr apps import files to here
│   │   ├── movies # Radarr
│   │   ├── music # Lidarr
│   │   └── tv # Sonarr
│   ├── torrents # Bittorrent client will put completed downloads here
│   │   ├── books
│   │   ├── movies
│   │   ├── music
│   │   └── tv
│   └── usenet
│       ├── complete # Usenet client will put completed downloads here
│       │   ├── books
│       │   ├── movies
│       │   ├── music
│       │   └── tv
│       ├── incomplete # Usenet client will put incomplete downloads here
│       └── watch # Usenet client will watch this for manually downloaded NZBs
│       │   ├── books # Named directories here match categories in SABnzbd
│       │   ├── movies
│       │   ├── music
│       │   └── tv
├── prowlarr
│   └── config
├── radarr
│   └── config
├── sabnzbd
│   └── config
├── sonarr
│   └── config
└── vpn # Not implemented yet
    └── config
```

Be sure to:

1.   Copy `.env.example` to `.env` at the project root.
2.   Set `TF_ROOT` to your host path (example on Windows: `C:/torrent_fiesta`).
3.   Optionally override paths:
     - `TF_DATA_DIR` (defaults to `<TF_ROOT>/data`)
     - `TF_CONFIG_DIR` (defaults to `<TF_ROOT>`)
     - `TF_IMPORTS_DIR` (defaults to `<TF_ROOT>/imports`)
4.   Set `TF_TZ` to your timezone.
5.   Optionally set `TF_TRANSMISSION_EXE` on Windows if Transmission is installed in a non-default location.

You can create this structure automatically with scripts in `scripts/`:

macOS/Linux shell:

```shell
./scripts/create_structure_macos.sh /Volumes/Pteri/torrent_fiesta
```

Windows PowerShell:

```powershell
.\scripts\create_structure_windows.ps1 -RootPath C:/torrent_fiesta
```

**NOTE:** The apps running in Docker containers will need access to these directories. Pay attention to `Remote Path Mappings` in the individual [Servarr app](#servarr-apps) sections below and you should not have to fiddle with `PUID`, `PGID`, and `UNMASK` settings in the Docker Compose files.

## To Start

Run the following **at the root level** of this project to start the app:

```shell
source .venv/bin/activate
```

or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

**NOTE:** This needs to be run to activate the environment setup in [Python](#python) in any new shell instance.

```shell
python3 main.py
```

or on Windows PowerShell:

```powershell
python main.py
```

or&mdash;better&mdash;create an alias like this and run it:

```shell
alias tfiesta="cd ~/projects/torrent-fiesta && source .venv/bin/activate && python3 main.py"
```

Either of these wll launch the app and attempt to start Docker and Transmission if they are not running, after which the CLI menu is presented.

### Runtime Options

Set these in `.env`:

- `TF_BROWSER_MODE=default|chrome` (`default` uses your system browser)
- Recommended on Windows for this app's tab workflow: `TF_BROWSER_MODE=chrome`
- `TF_ENABLE_UI_CLOSE=true|false` (attempts closing app tabs on quit when supported)
- `TF_TRANSMISSION_MODE=auto|manual`
- `TF_TRANSMISSION_EXE` (optional explicit Windows path to `transmission-qt.exe`)
- `TF_DATA_DIR` (optional, default: `<TF_ROOT>/data`)
- `TF_CONFIG_DIR` (optional, default: `<TF_ROOT>`)
- `TF_IMPORTS_DIR` (optional, default: `<TF_ROOT>/imports`)

## Compose Commands (No CLI)

You can run services directly with Docker Compose:

```shell
docker compose -p torrent_fiesta -f docker/services/movies/compose.yaml up -d
docker compose -p torrent_fiesta -f docker/services/tv/compose.yaml up -d
docker compose -p torrent_fiesta -f docker/services/full_service/compose.yaml up -d
docker compose -p torrent_fiesta down
```

## The CLI Menu

This should be fairly intuitive, but here's a few clarifications:

-   You can run individual Servarr apps (e.g. TV Shows/Sonar) or select `Full Service` to run them all at once.
-   All apps run in individual containers, including [Prowlarr](#prowlarr-setup) and [SABnzbd](#sabnzbs).
-   When you quit Torrent Fiesta, it should gracefully shut down all Docker containers.
-   If you break out of Torrent Fiesta with `CTRL+C` (or the app crashes) the Docker Compose project and its containers will continue running.
-   This _may_ cause issues when trying to run Torrent Fiesta again; however, there's some error handling to detect and recover from most situations.
-   If there's a scenario that isn't handled, you'll need to stop the running Docker Compose project and manually remove it.

## Download Clients

### Transmission

This project is setup to use Transmission installed locally on your machine (not in a Docker container).

- By default (`TF_TRANSMISSION_MODE=auto`), Torrent Fiesta attempts to start Transmission.
- If auto-start fails, Torrent Fiesta prompts you to start it manually and retry.
- If you prefer manual mode, set `TF_TRANSMISSION_MODE=manual`.

### SABnzbs

SABnzbs is configured to run in a Docker container when selecting Books, Movies, TV, and Full Service in the [CLI Menu](#the-cli-menu).

Once that container is running, the SABnzbs UI can be reached at [http://localhost:8080](http://localhost:8080)

#### Setup

1. Click on the gear icon, then General
2. Make note of the API Key under security. You'll need that for [Prowlarr](#prowlarr-setup)
3. Click on Folders
4. Use `/data/usenet/incomplete` for Temporary Download Folder
5. Use `/data/usenet/complete` for Completed Download Folder
6. Use `/data/usenet/watch` for Watched Folder
7. Save your changes
8. Click on Categories
9. Add a new category for `books`
10. Add a new category for `redarr`
11. Leave the other categories intact.

## Usenet

-   You'll need a Usenet provider. These cost money (not a lot). Try [NewsDemon](https://members.newsdemon.com/?ref=12154258).
-   Once signed up, you will need the the following for [SABnzbd](#sabnzbs)
    -   username
    -   password
    -   server (e.g. news.newsdemon.com)

## Servarr Apps

### Prowlarr Setup

-   Read the [Prowlarr Quick Start Guide](https://wiki.servarr.com/prowlarr/quick-start-guide)
-   Read the [Usenet](#usenet) and [SABnzbs](#sabnzbs) sections if you intend to use Usenet
-   Set up some torrent feeds (these are suggestions):
    -   1337x and/or YTS for Movies
    -   EZTV for TV Shows
    -   [MAM](#helpful-links) for Books (private tracker)
-   Set up some NZB feeds (these are suggestions due to easy registration):
    -   [NZBFinder](https://nzbfinder.ws/register?ref=317367)
    -   [NZBGeek](https://nzbgeek.info)
    -   [NZBNoob](https://www.nzbnoob.com)

NZB trackers are mostly--if not all--private. You need to register with them to use them.
Each NAB indexer you add to Prowlarr will need an API Key provided once you sign in.

-   Setup Radarr and Sonarr under Settings => Apps
    -   Be sure to use your local IP address, not `localhost`, for Server fields
    -   Get the API keys from each app individually.
    -   Update Sync Categories according to your needs.
-   Edit the Standard Sync Profile or Create New
-   Test All Apps
-   Sync App Indexes

### Radarr Setup

-   Read the [Radarr Quick Start Guide](https://wiki.servarr.com/radarr/quick-start-guide)

#### Authentication

-   Choose Authentication Method
-   Choose Disabled for Local Addresses
-   Enter Username and Password

#### Media Management

-   Enable Rename Episodes
-   Root Folders should include `/data/media`

#### Indexers

-   Copy the `API Key` from Settings => General
-   Add that to the Radarr App in Prowlarr

#### Download Clients

-   Click the + and select Transmission
    -   Enter your IP address in the Host field (e.g. 192.168.1.101)
    -   Set `Directory` to your equivalent of `<TF_ROOT>/data/torrents/movies`
        -   This overrides the settings in the Bittorrent client and puts the downloads where Radarr can find and import them.
    -   Test and Save
-   Under Remote Path Mappings, click the +
    -   Select your IP address in the Host field (e.g. 192.168.1.101)
    -   For Remote Path, enter your equivalent to `<TF_ROOT>/data/torrents/movies/`
    -   For Local Path, select `/data/torrents/movies/`


### Readarr 

- [Readarr has been retired](https://readarr.com/) and is no longer a part of Torrent Fiesta.

### Sonarr Setup

-   Read the [Sonarr Quick Start Guide](https://wiki.servarr.com/sonarr/quick-start-guide).

#### Authentication

-   Choose Authentication Method
-   Choose Disabled for Local Addresses
-   Enter Username and Password

#### Media Management

-   Enable Rename Episodes
-   Root Folders should include `/data/media`

#### Indexers

-   Copy the `API Key` from Settings => General
-   Add that to the Sonarr App in Prowlarr

#### Download Clients

-   Click the + and select Transmission
    -   Enter your IP address in the Host field (e.g. 192.168.1.101)
    -   Set `Directory` to your equivalent of `<TF_ROOT>/data/torrents/tv`
        -   This overrides the settings in the Bittorrent client and puts the downloads where Sonarr can find and import them.
    -   Test and Save
-   Under Remote Path Mappings, click the +
    -   Select your IP address in the Host field (e.g. 192.168.1.101)
    -   For Remote Path, enter your equivalent to `<TF_ROOT>/data/torrents/tv/`
    -   For Local Path, select `/data/torrents/tv/`

## Issues

### General

-   Auto selected Bittorrent downloads will often have very few seeders.
    -   Apparently some indexers lie about how many seeders there are.
    -   Interactive search can sometimes yield better results.
    -   Setting the Minimum Seeders value in Prowler => Apps => Sync Profiles may yield better results.
-   Opening Media locations does not bring Finder to the foreground, unless a window is already opened to the path and it has been minimized (I think that's the case). Not a big deal, but weird.
-   Browser tab close automation is fully supported on macOS with Chrome mode (`TF_BROWSER_MODE=chrome`).
-   On Windows, URL opening is supported. Chrome tab close is best-effort and may leave tabs open.
-   Not sure if this is true yet, but it appears that if single Servarr service is chosen (e.g. Sonarr), rather than Full Service, Prowlarr will fail due to inability to connect to non-started Apps. This will affect the chosen app and cause searches to fail.
    -   Workaround 1: Separate Prowlarr configs
    -   Workaround 2: Get rid of individual Servarr options and only use Full Service



## Documentation

-   [Servarr Wiki](https://wiki.servarr.com/)
-   [Radarr Quick Start Guide](https://wiki.servarr.com/radarr/quick-start-guide)

-   [Sonarr Quick Start Guide](https://wiki.servarr.com/sonarr/quick-start-guide).
-   [Servarr Docker Guide](https://wiki.servarr.com/docker-guide)
-   [SABnzbd Getting Started Guide](https://sabnzbd.org/wiki/introduction/quick-setup)

## Helpful Links

-   [Anna's Archive](https://annas-archive.org/slow_download/3c96b400b952b3f0ba050b21183a4912/0/0) is stand alone site for sourcing ebooks.
-   [Guide to Jackett](https://www.rapidseedbox.com/blog/guide-to-jackett)
-   [Hardlinks and Instant Moves (Atomic-Moves)](https://trash-guides.info/Hardlinks/Hardlinks-and-Instant-Moves/)
-   [How does completed download handling work?](https://www.reddit.com/r/radarr/comments/ghw6sq/how_does_completed_download_handling_work/)
-   [How to get invited to MAM](https://www.myanonamouse.net/chathelp.php).
-   [How to route any Docker container through a VPN container](https://www.youtube.com/watch?v=znSu_FuKFW0)
-   [Sonarr Troubleshooting](https://wiki.servarr.com/sonarr/troubleshooting)

## To Do

-   Implement Lidarr and Whisparr
-   Implement Plex Automation/Integration
-   Implement VPN container to route Bittorrent and Usenet traffic through

## Thoughts

-   One of the best things about using ServeArr apps is that it puts a layer between the user and torrent indexer sites. This means no more ads, popups and other annoying and potentially malicious things.
-   Torrent indexers are not very good for books, except for perhaps [MyAnonaMouse](https://www.myanonamouse.net).
-   While MyAnonaMouse seems to be a great source for books, Many releases require VIP status, which takes a long time to get, unless you pay for it.  This may be a worthwhile investment; however, many books, including new releases, are readily available via Usenet.
-   Nearly all--if not all--NZB indexers are private and paid. This means no ads, popups, etc.
