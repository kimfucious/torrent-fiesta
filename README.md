# Torrent Fiesta 🎉

This is a project to simplify running [Servarr](https://wiki.servarr.com/) apps in Docker containers.

All of this was created to run on a Mac and the documentation herein is macOS centric. If you're on another platform, some things just won't work.

At present, [Lidarr](https://wiki.servarr.com/en/lidarr) and [Whisparr](https://wiki.servarr.com/en/whisparr) are not implemented.

Python is used to provide a CLI for running the app and performing various tasks like launching apps (e.g. Docker & Transmission), opening Servarr apps in browser tabs, and upping/downing Docker compose projects.

[Prowler](https://prowlarr.com/) is used to manage indexers here, but [Jackett](https://github.com/Jackett/Jackett) could be easily swapped in.

While this project could be taken further to integrate with a media server (e.g. [Plex](https://www.plex.tv/)), that has not been done or documented (yet).

This project assumes the use of [Transmission](https://transmissionbt.com/) as a Bittorrent client, but using something else should not be that hard to do.

**!!! WARNING !!!:** Encapsulation of network traffic with a VPN is not implemented (yet), running this project will probably get you into trouble with your ISP and possibly other entities in most countries.

## Prerequisites

-   Read the [documentation](#documentation).
-   The information found in [Helpful Links](#helpful-links) can be useful as well, esp. if you get stuck.

### Docker

-   If not already installed, install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/).

Docker is used to run the Servarr apps in containers. The Compose files are located in the docker directory at the root level of this project.

The app will select the correct files to use to run compose up/down commands based on CLI Menu selections.

You can run Servarr apps individually or select `Full Service` to run them all at once. 

If you don't want a specific Servarr app to run in full service, edit the `full-service.compose.yaml` file, commenting out or deleting the service you do not wish to use.

### Python

-   Install Python 3 and pip (I use [Homebrew](https://docs.brew.sh/Homebrew-and-Python)).
-   In terminal, navigate to the root of this project and run the following commands to install dependencies in an isolated environment:

```console
> python3 -m venv .venv
> source .venv/bin/activate 
> python3 -m pip install -r requirements.txt
```

**NOTE:** The `.venv` directory and its subdirectories are excluded in `.gitignore`.

### Folder Structure

Create a folder structure like this on your local machine:

```shell
    ├── data
    │   ├── media # Servarr apps put imported files here
    │   │   ├── books # readarr
    │   │   ├── movies # radarr
    │   │   └── tv # sonarr
    │   └── torrents # Bittorrent client will put completed downloads here
    │       ├── books
    │       ├── movies
    │       └── tv
    ├── prowlarr
    │   ├── config
    ├── radarr
    │   └── config
    ├── readarr
    │   └── config
    └── sonarr
        └── config
```

I have this entire structure in a directory called `torrent_fiesta` on `/Volumes/Pteri`.

`/Volumes/Pteri` is a USB attached drive on _my machine_.

Be sure to:

-   Use what's appropriate for your environment and update the `volumes` sections in the Docker compose files in the `docker/xarr` directory accordingly.
-   Update the `app_root_on_disk` value in `global.py` to match your environment.

**NOTE:** The Servarr apps running in Docker containers will need access to these directories. Pay attention to `Remote Path Mappings` in the individual [Servarr app](#servarr-apps) sections below and you should not have to fiddle with `PUID`, `PGID`, and `UNMASK` settings in the Docker Compose files.

## To Start

Run the following at the root level of this project to start the app:

```shell
source .venv/bin/activate
```

```shell
python3 main.py
```

or create an alias like this and run it:

```shell
alias torrents="cd ~/projects/torrent-fiesta && source .venv/bin/activate && python3 main.py"
```

Either of these wll launch the app and attempt to start Docker and Transmission if they is not running, after which a CLI menu is presented.

## The CLI Menu

This should be fairly intuitive, but here's a few clarifications:

-   You can run individual Servarr apps or select `Full Service` to run them all at once.
-   When you quit the app, it should gracefully shut down.
-   If you break out of the app with `CTRL+C` (or the app crashes) the Docker Compose project and its containers will continue running.
-   This _may_ cause issues when trying to run the app again; however, there's some error handling in the app to detect and recover from most situations.
-   If there's a scenario that isn't handled, you'll need to stop the running Docker Compose project and manually remove it.

## Servarr Apps

### Prowlarr

-   Read the [Prowlarr Quick Start Guide](https://wiki.servarr.com/prowlarr/quick-start-guide)
-   Set up some feeds (these are suggestions):
    -   1337x and/or YTS for Movies
    -   EZTV for TV Shows
    -   [MAM](#helpful-links) for Books (private tracker)
-   Setup Radarr, Readarr, and Sonarr under Settings => Apps
    -   Be sure to use your local IP address, not `localhost` for Server fields
    -   Get the API keys from each app individually.
    -   Update Sync Categories according to your needs.
-   Edit the Standard Sync Profile or Create New
-   Test All Apps
-   Sync App Indexes

The above is for Torrents only. Docs for Usenet are not added yet.

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
    -   Set `Directory` to your equivalent of `/Volumes/Pteri/torrent_fiesta/data/torrents/movies`
        -   This overrides the settings in the Bittorrent client and puts the downloads where Radarr can find and import them.
    -   Test and Save
-   Under Remote Path Mappings, click the +
    -   Select your IP address in the Host field (e.g. 192.168.1.101)
    -   For Remote Path, enter your equivalent to `/Volumes/Pteri/torrent_fiesta/data/torrents/movies/`
    -   For Local Path, select `/data/torrents/movies/`

### Readarr Setup

-   Read the [Readarr Quick Start Guide](https://wiki.servarr.com/readarr/quick-start-guide)

#### Authentication

-   Choose Authentication Method
-   Choose Disabled for Local Addresses
-   Enter Username and Password

#### Media Management

**NOTE:** Readarr is a bit different than the others so pay attention.

-   Add a Remote Path Mapping
    -   Host: your local IP address (e.g. 192.168.1.101)
    -   Remote Path: Your equivalent of `/Volumes/Pteri/torrent_fiesta/data/torrents/books/`
    -   Local Path: `/data/torrents/books/`
-   Enable Rename Episodes

#### Indexers

-   Copy the `API Key` from Settings => General
-   Add that to the Radarr App in Prowlarr

#### Download Clients

-   Under Remote Path Mappings, click the +
    -   Select your IP address in the Host field (e.g. 192.168.1.101)
    -   For Remote Path, enter your equivalent to `/Volumes/Pteri/torrent_fiesta/data/torrents/books/`
    -   For Local Path, select `/data/torrents/books/`

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
    -   Set `Directory` to your equivalent of `/Volumes/Pteri/torrent_fiesta/data/torrents/tv`
        -   This overrides the settings in the Bittorrent client and puts the downloads where Sonarr can find and import them.
    -   Test and Save
-   Under Remote Path Mappings, click the +
    -   Select your IP address in the Host field (e.g. 192.168.1.101)
    -   For Remote Path, enter your equivalent to `/Volumes/Pteri/torrent_fiesta/data/torrents/tv/`
    -   For Local Path, select `/data/torrents/tv/`

## Issues

### General

-   Auto selected downloads will often have very few seeders.
    -   Apparently some indexers lie about how many seeders there are.
    -   Interactive search can sometimes yield better results.
    -   Setting the Minimum Seeders value in Prowler => Apps => Sync Profiles may yield better results.
-   Opening Media locations does not bring Finder to the foreground, unless a window is already opened to the path and it has been minimized (I think that's the case). Not a big deal, but weird.
-   Not sure if this is true yet, but it appears that if single Servarr service is chosen (e.g. Sonarr), rather than Full Service, Prowlarr will fail due to inability to connect to non-started Apps. This will affect the chosen app and cause searches to fail.
    -   Workaround 1: Separate Prowlarr configs
    -   Workaround 2: Get rid of individual Servarr options and only use Full Service

### Readarr

-   Does not work very well using torrent trackers.
-   Prolly need to setup Usenet tracker for ebooks, as torrents do not seem to source well.
-   [MyAnonamouse](https://www.myanonamouse.net/) is a private tracker that requires an invite, which may improve things for torrents.
-   [Anna's Archive](https://www.myanonamouse.net/) is an alternative source for ebooks, but does not work with Readarr.

## Documentation

-   [Servarr Wiki](https://wiki.servarr.com/)
-   [Radarr Quick Start Guide](https://wiki.servarr.com/radarr/quick-start-guide)
-   [Readarr Quick Start Guide](https://wiki.servarr.com/readarr/quick-start-guide)
-   [Sonarr Quick Start Guide](https://wiki.servarr.com/sonarr/quick-start-guide).
-   [Servarr Docker Guide](https://wiki.servarr.com/docker-guide)

## Helpful Links

-   [Anna's Archive](https://annas-archive.org/slow_download/3c96b400b952b3f0ba050b21183a4912/0/0) is stand alone site for sourcing ebooks.
-   [Guide to Jackett](https://www.rapidseedbox.com/blog/guide-to-jackett)
-   [Hardlinks and Instant Moves (Atomic-Moves)](https://trash-guides.info/Hardlinks/Hardlinks-and-Instant-Moves/)
-   [How does completed download handling work?](https://www.reddit.com/r/radarr/comments/ghw6sq/how_does_completed_download_handling_work/)
-   [How to get invited to MAM](https://www.myanonamouse.net/chathelp.php).
-   [How to route any Docker container through a VPN container](https://www.youtube.com/watch?v=znSu_FuKFW0)
-   [Sonarr Troubleshooting](https://wiki.servarr.com/sonarr/troubleshooting)
