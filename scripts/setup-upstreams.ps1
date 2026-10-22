# Windows PowerShell: requires Git installed. Fetch only selected real upstream sources.
param(
    [ValidateSet('UnityPy','Grasscutter','LunarCore','godot-demo-projects','all')]
    [string]$Project = 'UnityPy'
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo
$projects = if ($Project -eq 'all') { @('UnityPy','Grasscutter','LunarCore','godot-demo-projects') } else { @($Project) }
foreach ($name in $projects) {
    Write-Host "Fetching pinned upstream: $name"
    git submodule update --init -- third_party/$name
    if ($LASTEXITCODE -ne 0) { throw "git submodule update failed for $name" }
}
Write-Host 'Pinned upstream sources available under third_party/.'
Write-Host 'Third-party licenses and code remain owned by their upstream authors.'
