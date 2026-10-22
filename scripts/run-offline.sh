#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
git submodule update --init -- third_party/godot-demo-projects
python3 offline_game/tools/build_game.py --force
if test "$#" -gt 0 && test "$1" = "--build-only"; then
  echo "Built offline_game/build/solo_jrpg/project.godot"
  exit 0
fi
exec godot --path offline_game/build/solo_jrpg
