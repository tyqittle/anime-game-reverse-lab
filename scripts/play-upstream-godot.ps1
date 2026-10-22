# Launch an EXISTING upstream open-source game, not the custom browser prototype.
param(
    [ValidateSet('platformer','jrpg')]
    [string]$Game = 'platformer',
    [string]$Godot = 'godot'
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$project = Join-Path $root "third_party/godot-demo-projects/2d/$Game"
if (-not (Test-Path (Join-Path $project 'project.godot'))) {
    throw "Open-source game source absent. First run: git submodule update --init -- third_party/godot-demo-projects"
}
if (-not (Get-Command $Godot -ErrorAction SilentlyContinue)) {
    throw "Godot executable not found. Install Godot Engine 4 or specify -Godot 'C:\path\to\Godot.exe'."
}
Write-Host "Starting real Godot demo source: $project"
& $Godot --path $project
exit $LASTEXITCODE
