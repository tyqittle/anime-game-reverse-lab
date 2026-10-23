# Windows PC: launches a pinned, real Arknights fan-made mode (not the official Arknights client).
# Default: no asset download, bind localhost only. Third-party license: GPL-3.0-or-later.
param(
  [switch]$AllowAssetDownloads,
  [switch]$SkipInstall,
  [ValidateRange(1024,65535)][int]$Port = 3000
)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$game = Join-Path $root "third_party/Arknights-Stronghold-Protocol"
$project = Join-Path $game "package.json"
if (!(Get-Command git -ErrorAction SilentlyContinue)) { throw "Git required: https://git-scm.com/download/win" }
if (!(Test-Path $project)) {
    Push-Location $root
    try {
        git submodule update --init -- third_party/Arknights-Stronghold-Protocol
        if ($LASTEXITCODE -ne 0) { throw "Pinned upstream Git checkout failed." }
    } finally { Pop-Location }
}
if (!(Get-Command node -ErrorAction SilentlyContinue)) { throw "Node.js >=22 required: https://nodejs.org/" }
$nodeMajor = [int]((& node -p "process.versions.node.split('.')[0]").Trim())
if ($nodeMajor -lt 22) { throw "Node.js 22+ required, current $nodeMajor" }
Push-Location $game
try {
    if (!$SkipInstall -and !(Test-Path "node_modules/ws/package.json")) {
        Write-Host "Installing official upstream Node dependencies from package-lock.json..."
        npm ci --no-audit --no-fund
        if ($LASTEXITCODE -ne 0) { throw "npm ci failed." }
    }
    $args = @("scripts/launch.mjs", "--host", "127.0.0.1", "--port", [string]$Port, "--no-local", "--no-scenes", "--scripts", "off", "--test-mode", "off")
    if (!$AllowAssetDownloads) {
        # Warn: first-run artwork/audio may be incomplete without the upstream assets.
        Write-Warning "Running with --no-assets. Some game art/Spine/audio can be missing on first launch."
        $args += "--no-assets"
    } else {
        Write-Warning "AllowAssetDownloads enables upstream's first-run art fetch (about 720 MB). Assets are third-party copyrighted, not committed to this repository."
    }
    Write-Host "Starting Arknights STRONGHOLD mode at http://127.0.0.1:$Port"
    Write-Host "This is an independent fan-made game mode, NOT a local login for the official game."
    & node @args
    if ($LASTEXITCODE -ne 0) { throw "Upstream launch failed with code $LASTEXITCODE" }
} finally { Pop-Location }
