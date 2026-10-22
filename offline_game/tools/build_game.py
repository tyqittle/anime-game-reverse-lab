"""Build an editable, offline JRPG from genuine pinned Godot demo source (MIT).

The original demo supplies movement, scenes, dialog, monsters, battles and art.
We copy it unmodified, then add a local-only save/pause autoload.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ORIGIN = Path("third_party/godot-demo-projects/2d/role_playing_game")
LICENSE = Path("third_party/godot-demo-projects/LICENSE.md")
OVERLAY = Path("offline_game/overlay")
OUTPUT = Path("offline_game/build/solo_jrpg")
UPSTREAM_REVISION = "b761b4cd5718a7118f2c95eb55f181d0a5f004f1"
AUTOLOAD = 'OfflineManager="*res://addons/offline_mode/offline_manager.gd"'

def configure(contents: str) -> str:
    if "[application]" not in contents or "run/main_scene=" not in contents:
        raise ValueError("The official project.godot is missing expected sections.")
    contents, found = re.subn(r'^config/name=.*$', 'config/name="Offline JRPG - Solo Adventure"',
                              contents, count=1, flags=re.MULTILINE)
    if not found:
        raise ValueError("Upstream config lacks an app name.")
    if AUTOLOAD not in contents:
        if "[autoload]" in contents:
            contents = contents.replace("[autoload]", "[autoload]\n" + AUTOLOAD, 1)
        else:
            contents += "\n[autoload]\n\n" + AUTOLOAD + "\n"
    return contents

def _ignore(directory: str, entries: list[str]) -> list[str]:
    return [e for e in entries if e in {".godot", ".git", ".DS_Store", "screenshots"}]

def build(root: Path, out: Path | None = None, force: bool = False) -> dict:
    root = root.resolve()
    source = root / ORIGIN
    destination_input = out or root / OUTPUT
    if destination_input.is_symlink():
        raise ValueError("Refusing symlink output directory.")
    destination = destination_input.resolve()
    allowed = (root / "offline_game/build").resolve()
    if destination == allowed or not destination.is_relative_to(allowed):
        raise ValueError("Output must be a subfolder of offline_game/build/.")
    if not (source / "project.godot").is_file():
        raise FileNotFoundError("Missing official game source. Run git submodule update --init -- third_party/godot-demo-projects")
    if not (root / LICENSE).is_file():
        raise FileNotFoundError("Missing upstream copyright license.")
    if not (root / OVERLAY / "addons/offline_mode/offline_manager.gd").is_file():
        raise FileNotFoundError("Missing offline mode addon.")
    if destination.exists() and not force:
        raise FileExistsError(f"Project already built at {destination}; use --force.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=".offline-game-", dir=destination.parent))
    try:
        shutil.copytree(source, temp, dirs_exist_ok=True, ignore=_ignore)
        shutil.copytree(root / OVERLAY, temp, dirs_exist_ok=True)
        project = temp / "project.godot"
        project.write_text(configure(project.read_text(encoding="utf-8")), encoding="utf-8")
        shutil.copy2(root / LICENSE, temp / "UPSTREAM_LICENSE.md")
        (temp / "OFFLINE_ORIGIN.json").write_text(json.dumps({
            "upstream": "https://github.com/godotengine/godot-demo-projects",
            "commit": UPSTREAM_REVISION,
            "source_project": ORIGIN.as_posix(),
            "changes": ["local save/pause Autoload", "application display name"],
            "network_login": False
        }, indent=2) + "\n", encoding="utf-8")
        if destination.exists():
            shutil.rmtree(destination)
        temp.replace(destination)
        return {"project": str(destination / "project.godot"),
                "main_scene": "res://game.tscn", "save": "user://offline_game/slot1.json"}
    finally:
        if temp.exists():
            shutil.rmtree(temp)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a real upstream Godot RPG with offline save/pause")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(build(args.root, args.out, args.force), indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
