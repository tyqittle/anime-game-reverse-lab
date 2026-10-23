"""Build Arknights-inspired PC tower-defense proof of concept from real MIT Godot game.

Gameplay systems (enemies, pathfinding, turrets, projectiles and waves) stay from
quiver-dev/tower-defense-godot4 at a pinned SHA. This tool layers a launcher,
local progress and optionally *user-supplied* portrait/chibi files over them.
It never writes into the upstream submodule or downloads copyrighted images.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

UPSTREAM = Path("third_party/arknights-td-godot")
OVERLAY = Path("arknights_pc/overlay")
OUTPUT = Path("arknights_pc/build/arknights_td")
REV = "1cbd622116dbf5acc0f284f57ece22970338afe8"
EXTS = {".png", ".jpg", ".jpeg", ".webp"}
NAME_KEYS = ("characterName", "name", "nameZh", "nameEn")
IMAGE_KEYS = ("localPath", "localImage", "imagePath", "image", "portrait", "fullImage", "imageUrl", "src", "path", "filePath", "url")


def _safe_local(root: Path, value: str) -> Path | None:
    if not value or "://" in value or value.startswith(("data:", "//")):
        return None
    candidate = (root / value.removeprefix("./")).resolve()
    if not candidate.is_relative_to(root.resolve()) or candidate.suffix.lower() not in EXTS:
        return None
    if not candidate.is_file() or candidate.stat().st_size > 18 * 1024 * 1024:
        return None
    return candidate


def _records(archive: Path) -> list[dict]:
    source = archive / "data/characters.json"
    if not source.is_file():
        return []
    data = json.loads(source.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [o for o in data if isinstance(o, dict)]
    if isinstance(data, dict):
        for key in ("characters", "entries", "items", "portraits"):
            if isinstance(data.get(key), list):
                return [o for o in data[key] if isinstance(o, dict)]
    return []


def _candidate_image(archive: Path, obj: dict) -> Path | None:
    for key in IMAGE_KEYS:
        value = obj.get(key)
        if not isinstance(value, str):
            continue
        found = _safe_local(archive, value)
        if found:
            return found
        # Manifest may store the basename rather than assets/portraits/...
        if "/" not in value and "\\" not in value:
            found = _safe_local(archive, f"assets/portraits/{value}")
            if found:
                return found
    # Explicitly consider the original id when images live in assets/portraits/.
    stem = str(obj.get("id", ""))
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,120}", stem):
        return None
    for ext in EXTS:
        found = _safe_local(archive, f"assets/portraits/{stem}{ext}")
        if found:
            return found
    return None



# Three portraits known to exist in the user's published archive. Artwork is
# fetched to the USER'S LOCAL BUILD ONLY, never committed or shipped via CI.
PUBLIC_GALLERY = "https://raw.githubusercontent.com/tyqittle/anime-character-archive/main/assets/portraits/"
STARTER_PORTRAITS = (
    ("芬", "ak-char_123_fang-1.webp"),
    ("能天使", "ak-char_103_angel-1.webp"),
    ("阿米娅", "ak-char_002_amiya-1.webp"),
)


def fetch_public_gallery_art(dest: Path, manifest: dict) -> int:
    """Optional install-time download of three user-archive portraits, not runtime CDN dependency."""
    import urllib.request
    copied = 0
    folder = dest / "arknights/assets/portraits"
    folder.mkdir(parents=True, exist_ok=True)
    for i, (name, filename) in enumerate(STARTER_PORTRAITS):
        target = folder / f"slot_{i}.webp"
        try:
            request = urllib.request.Request(PUBLIC_GALLERY + filename,
                                             headers={"User-Agent": "ArknightsLocalLab/0.1"})
            with urllib.request.urlopen(request, timeout=20) as response:
                data = response.read(8 * 1024 * 1024 + 1)
            if len(data) > 8 * 1024 * 1024 or not (data[:4] == b"RIFF" and data[8:12] == b"WEBP"):
                raise ValueError(f"Not a bounded WebP image: {filename}")
            target.write_bytes(data)
            entry = manifest["slots"][i]
            entry["name"] = name
            entry["portrait"] = f"res://arknights/assets/portraits/slot_{i}.webp"
            entry["source"] = f"tyqittle/anime-character-archive:{filename}"
            copied += 1
        except (OSError, ValueError) as exc:
            print(f"Warning: portrait unavailable ({filename}): {exc}", file=sys.stderr)
    (dest / "arknights/assets/manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return copied


def import_art(dest: Path, archive: Path | None, chibi: Path | None) -> dict:
    art_root = dest / "arknights" / "assets"
    (art_root / "portraits").mkdir(parents=True, exist_ok=True)
    (art_root / "chibi").mkdir(parents=True, exist_ok=True)
    slots = [
        {"id": "slot_0", "role": "先锋（近战演示）", "turret": "gatling", "name": "先锋"},
        {"id": "slot_1", "role": "狙击（远程演示）", "turret": "single", "name": "狙击"},
        {"id": "slot_2", "role": "术师（范围演示）", "turret": "missile", "name": "术师"},
    ]
    if archive:
        archive = archive.resolve()
        matches = [x for x in _records(archive)
                   if str(x.get("gameId", x.get("game", ""))).lower() in {"arknights", "明日方舟"}]
        seen: set[str] = set()
        chosen = []
        for obj in matches:
            path = _candidate_image(archive, obj)
            identity = str(obj.get("characterKey") or obj.get("characterName") or obj.get("name") or obj.get("id", ""))
            if not path or not identity or identity in seen:
                continue
            seen.add(identity)
            chosen.append((obj, path))
            if len(chosen) == len(slots):
                break
        for index, (entry, path) in enumerate(chosen):
            extension = path.suffix.lower()
            name = f"slot_{index}{extension}"
            shutil.copy2(path, art_root / "portraits" / name)
            slots[index]["portrait"] = f"res://arknights/assets/portraits/{name}"
            slots[index]["name"] = str(next((entry[k] for k in NAME_KEYS if isinstance(entry.get(k), str) and entry[k]), slots[index]["name"]))[:64]
            slots[index]["source"] = path.relative_to(archive).as_posix()
    if chibi:
        chibi = chibi.resolve()
        if not chibi.is_dir():
            raise FileNotFoundError(f"No chibi input directory: {chibi}")
        for i in range(3):
            for name in (f"slot_{i}.png", f"operator_{i}.png", f"slot_{i}.webp"):
                source = _safe_local(chibi, name)
                if source:
                    target = f"slot_{i}{source.suffix.lower()}"
                    shutil.copy2(source, art_root / "chibi" / target)
                    slots[i]["chibi"] = f"res://arknights/assets/chibi/{target}"
                    break
    manifest = {"version": 1, "source": "local-only", "slots": slots,
                "notice": "Artwork and chibi rights stay with their original owners; files are never committed."}
    (art_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def _ignore(_directory: str, names: list[str]) -> set[str]:
    return {n for n in names if n in {".git", ".godot", ".DS_Store"}}


def build(root: Path, archive: Path | None = None, chibi: Path | None = None,
          force: bool = False, fetch_gallery: bool = False) -> dict:
    root = root.resolve()
    src = root / UPSTREAM
    overlay = root / OVERLAY
    target = root / OUTPUT
    if not (src / "project.godot").is_file() or not (src / "scenes/maps/map_template.tscn").is_file():
        raise FileNotFoundError("Missing pinned Outpost Assault source: git submodule update --init -- third_party/arknights-td-godot")
    if not (src / "LICENSE.txt").is_file():
        raise FileNotFoundError("Upstream source has no LICENSE file: verify before building")
    if not (overlay / "arknights/launcher.tscn").is_file():
        raise FileNotFoundError("Overlay is missing.")
    if target.exists() and not force:
        raise FileExistsError("Build already exists; pass --force")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=".ark-td-", dir=target.parent))
    try:
        shutil.copytree(src, tmp, dirs_exist_ok=True, ignore=_ignore)
        shutil.copytree(overlay, tmp, dirs_exist_ok=True)
        cfg = (tmp / "project.godot").read_text(encoding="utf-8")
        if 'run/main_scene="res://interfaces/UI/menu/menu.tscn"' not in cfg:
            raise ValueError("Upstream main scene changed; rebase adapter instead of guessing")
        cfg = cfg.replace('config/name="Outpost Assault"', 'config/name="方舟离线战术试验场"')
        cfg = cfg.replace('run/main_scene="res://interfaces/UI/menu/menu.tscn"', 'run/main_scene="res://arknights/launcher.tscn"')
        if "[autoload]" not in cfg:
            raise ValueError("Missing base game autoloads")
        cfg = cfg.replace("[autoload]", '[autoload]\nAKBridge="*res://arknights/bridge.gd"')
        (tmp / "project.godot").write_text(cfg, encoding="utf-8")
        art = import_art(tmp, archive, chibi)
        if fetch_gallery and archive is None:
            fetch_public_gallery_art(tmp, art)
        license_path = src / "LICENSE.txt"
        shutil.copy2(license_path, tmp / "UPSTREAM_LICENSE.txt")
        if (src / "LICENSE_ASSETS.txt").is_file():
            shutil.copy2(src / "LICENSE_ASSETS.txt", tmp / "UPSTREAM_ASSETS_LICENSE.txt")
        (tmp / "AK_ORIGIN.json").write_text(json.dumps({
            "upstream": "https://github.com/quiver-dev/tower-defense-godot4",
            "commit": REV, "upstream_scene": "res://scenes/maps/map_template.tscn",
            "engine_reused": ["enemy AI", "turret detection", "projectiles", "wave spawner", "navigation", "HUD"],
            "modifications": ["offline launcher", "portrait/chibi art bindings", "progress persistence", "deployment point economy"],
            "original_arknights_client": False
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if target.exists():
            shutil.rmtree(target)
        tmp.replace(target)
        return {"build": str(target), "entry": "res://arknights/launcher.tscn",
                "upstream_revision": REV, "portrait_count": sum("portrait" in x for x in art["slots"]),
                "chibi_count": sum("chibi" in x for x in art["slots"])}
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Offline Godot Arknights-inspired tower-defense builder")
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--archive", type=Path, help="local checkout of tyqittle/anime-character-archive")
    p.add_argument("--chibi", type=Path, help="local directory containing slot_0.png, slot_1.png and slot_2.png")
    p.add_argument("--force", action="store_true")
    p.add_argument("--fetch-gallery-art", action="store_true", help="Download three curated images only into local build; never into Git")
    a = p.parse_args(argv)
    try:
        print(json.dumps(build(a.root, a.archive, a.chibi, a.force, a.fetch_gallery_art), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
