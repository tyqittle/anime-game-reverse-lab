# Build and run the REAL Quiver Outpost Assault MIT tower-defense source with a local Arknights-style overlay.
param(
    [string]$Godot = "godot",
    [string]$Archive = "",
    [string]$Chibi = "",
    [switch]$BuildOnly
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git is required: https://git-scm.com/download/win" }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3.10+ is required." }
Write-Host "[1/3] Fetching real MIT tower-defense engine source..."
git submodule update --init -- third_party/arknights-td-godot
if ($LASTEXITCODE -ne 0) { throw "Upstream checkout failed" }
$cmdArgs = @("arknights_pc/tools/build.py", "--force")
if ($Archive -ne "") { $cmdArgs += @("--archive", $Archive) }
if ($Chibi -ne "") { $cmdArgs += @("--chibi", $Chibi) }
Write-Host "[2/3] Assembling playable local Godot project and optional portraits/chibi..."
& python @cmdArgs
if ($LASTEXITCODE -ne 0) { throw "Game builder failed" }
if ($BuildOnly) {
    Write-Host "Ready: arknights_pc/build/arknights_td/project.godot"
    exit 0
}
if (-not (Get-Command $Godot -ErrorAction SilentlyContinue) -and -not (Test-Path -LiteralPath $Godot)) {
    throw "Godot Engine 4.7+ not found. Install it or pass -Godot 'C:\path\Godot.exe'"
}
Write-Host "[3/3] Starting local, single-player game (no official login)..."
& $Godot --path "$root/arknights_pc/build/arknights_td"
exit $LASTEXITCODE
