#!/usr/bin/env bash
set -euo pipefail

ROOT_INPUT="${1:-${TF_ROOT:-}}"
if [[ -z "${ROOT_INPUT}" ]]; then
  echo "Usage: $0 <root_path>"
  echo "Or set TF_ROOT in your environment before running."
  exit 1
fi

ROOT="${ROOT_INPUT%/}"

dirs=(
  "data/media/movies"
  "data/media/music"
  "data/media/tv"
  "data/torrents/books"
  "data/torrents/movies"
  "data/torrents/music"
  "data/torrents/tv"
  "data/usenet/complete/books"
  "data/usenet/complete/movies"
  "data/usenet/complete/music"
  "data/usenet/complete/tv"
  "data/usenet/incomplete"
  "data/usenet/watch/books"
  "data/usenet/watch/movies"
  "data/usenet/watch/music"
  "data/usenet/watch/tv"
  "prowlarr/config"
  "radarr/config"
  "sabnzbd/config"
  "sonarr/config"
  "whisparr/config"
  "vpn/config"
  "imports/sonarr_tv"
)

for dir in "${dirs[@]}"; do
  mkdir -p "${ROOT}/${dir}"
done

echo "Created/verified Torrent Fiesta structure at: ${ROOT}"
