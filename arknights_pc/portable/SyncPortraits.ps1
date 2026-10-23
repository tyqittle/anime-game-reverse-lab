# Personal local cache of three portraits from the user's own public gallery.
# Does NOT republish images; once cached, launch works without network.
# Add your own Q images to game/arknights/assets/chibi/slot_0.png (or slot_1/slot_2).
param([switch]$Offline)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $PSScriptRoot).Path
$game = Join-Path $root 'game'
$assets = Join-Path $game 'arknights\assets'
$portraits = Join-Path $assets 'portraits'
$chibis = Join-Path $assets 'chibi'
$manifestPath = Join-Path $assets 'manifest.json'
if (-not (Test-Path $manifestPath)) { throw "Missing arknights assets/manifest.json in package" }
New-Item -ItemType Directory -Force -Path $portraits, $chibis | Out-Null
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$items = @(
    @{ Name = '芬'; Source = 'ak-char_123_fang-1.webp' },
    @{ Name = '能天使'; Source = 'ak-char_103_angel-1.webp' },
    @{ Name = '阿米娅'; Source = 'ak-char_002_amiya-1.webp' }
)
$dirty = $false
$attempted = Join-Path $assets ".portrait-fetch-attempted"
$allowFetch = (-not $Offline) -and (-not (Test-Path $attempted))
for ($i = 0; $i -lt 3; $i++) {
    $entry = $manifest.slots[$i]
    $dst = Join-Path $portraits "slot_$i.webp"
    if (-not (Test-Path $dst) -and $allowFetch) {
        $url = "https://raw.githubusercontent.com/tyqittle/anime-character-archive/main/assets/portraits/$($items[$i].Source)"
        $temporary = "$dst.download"
        try {
            Invoke-WebRequest -Uri $url -OutFile $temporary -TimeoutSec 20
            $bytes = [IO.File]::ReadAllBytes($temporary)
            if ($bytes.Length -gt 8MB -or $bytes.Length -lt 12 -or
                [Text.Encoding]::ASCII.GetString($bytes, 0, 4) -ne 'RIFF' -or
                [Text.Encoding]::ASCII.GetString($bytes, 8, 4) -ne 'WEBP') {
                throw 'Invalid image content'
            }
            Move-Item -LiteralPath $temporary -Destination $dst -Force
        } catch {
            Write-Warning "Portrait not fetched ($($items[$i].Name)). Using original MIT game art. $($_.Exception.Message)"
        } finally {
            Remove-Item -LiteralPath $temporary -ErrorAction SilentlyContinue
        }
    }
    if (Test-Path $dst) {
        $entry | Add-Member -NotePropertyName portrait -NotePropertyValue "res://arknights/assets/portraits/slot_$i.webp" -Force
        $entry | Add-Member -NotePropertyName name -NotePropertyValue $items[$i].Name -Force
        $dirty = $true
    }
    foreach ($ext in @('png', 'webp')) {
        $q = Join-Path $chibis "slot_$i.$ext"
        if (Test-Path $q) {
            $entry | Add-Member -NotePropertyName chibi -NotePropertyValue "res://arknights/assets/chibi/slot_$i.$ext" -Force
            $dirty = $true
            break
        }
    }
}
if ($allowFetch) {
    New-Item -ItemType File -Path $attempted -Force | Out-Null
}
if ($dirty) {
    $json = ConvertTo-Json -InputObject $manifest -Depth 10
    [IO.File]::WriteAllText($manifestPath, $json, [Text.UTF8Encoding]::new($false))
}
# Re-import only when portrait/Q picture files change (and never on ordinary launches).
$hashes = @()
Get-ChildItem -Path $portraits, $chibis -File | Sort-Object FullName | ForEach-Object {
    $hashes += "$($_.Name):$((Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash)"
}
$signature = $hashes -join '|'
$statePath = Join-Path $assets '.art-import-state'
$previous = if (Test-Path $statePath) { Get-Content -LiteralPath $statePath -Raw } else { '' }
if ($signature -ne $previous -and $signature -ne '') {
    & (Join-Path $root 'ArknightsLab.exe') --headless --path $game --editor --import --quit
    if ($LASTEXITCODE -eq 0) {
        [IO.File]::WriteAllText($statePath, $signature, [Text.UTF8Encoding]::new($false))
    } else {
        Write-Warning 'Art import did not complete; the base game can still launch.'
    }
}
