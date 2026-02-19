param(
    [Parameter(Mandatory = $false)]
    [string]$RootPath = $env:TF_ROOT
)

if ([string]::IsNullOrWhiteSpace($RootPath)) {
    Write-Host "Usage: .\scripts\create_structure_windows.ps1 -RootPath C:/torrent_fiesta" -ForegroundColor Yellow
    Write-Host "Or set TF_ROOT in your environment before running." -ForegroundColor Yellow
    exit 1
}

$trimChars = [char[]]@('/', '\')
$root = $RootPath.TrimEnd($trimChars)
if ([string]::IsNullOrWhiteSpace($root)) {
    Write-Host "RootPath resolved to an empty value after trimming. Please provide a valid path." -ForegroundColor Red
    exit 1
}
$dirs = @(
    "data/media/movies",
    "data/media/music",
    "data/media/tv",
    "data/torrents/books",
    "data/torrents/movies",
    "data/torrents/music",
    "data/torrents/tv",
    "data/usenet/complete/books",
    "data/usenet/complete/movies",
    "data/usenet/complete/music",
    "data/usenet/complete/tv",
    "data/usenet/incomplete",
    "data/usenet/watch/books",
    "data/usenet/watch/movies",
    "data/usenet/watch/music",
    "data/usenet/watch/tv",
    "prowlarr/config",
    "radarr/config",
    "sabnzbd/config",
    "sonarr/config",
    "whisparr/config",
    "vpn/config",
    "imports/sonarr_tv"
)

foreach ($dir in $dirs) {
    $target = Join-Path $root ($dir -replace '/', [IO.Path]::DirectorySeparatorChar)
    New-Item -ItemType Directory -Path $target -Force | Out-Null
}

Write-Host "Created/verified Torrent Fiesta structure at: $root" -ForegroundColor Green
