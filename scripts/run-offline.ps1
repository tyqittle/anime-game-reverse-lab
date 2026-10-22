# Requires Git, Python 3, and Godot compatible with the pinned upstream demo.
param([string]$Godot = "godot", [switch]$BuildOnly)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
Write-Host "[1/3] Obtaining real MIT-licensed JRPG source..."
git submodule update --init -- third_party/godot-demo-projects
if ($LASTEXITCODE -ne 0) { throw "Cannot fetch official JRPG source. Check network and Git." }
Write-Host "[2/3] Building standalone offline source..."
python offline_game/tools/build_game.py --force
if ($LASTEXITCODE -ne 0) { throw "Build failed; upstream has not been changed." }
if ($BuildOnly) {
  Write-Host "Godot project built: offline_game/build/solo_jrpg/project.godot"
  exit 0
}
if (-not (Get-Command $Godot -ErrorAction SilentlyContinue) -and -not (Test-Path -LiteralPath $Godot)) {
  throw "Godot executable not found. Install compatible Godot or provide -Godot C:\path\Godot.exe"
}
Write-Host "[3/3] Starting offline game..."
& $Godot --path "$root/offline_game/build/solo_jrpg"
exit $LASTEXITCODE
