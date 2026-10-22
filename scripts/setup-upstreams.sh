#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-UnityPy}" in
  all) git submodule update --init -- third_party/UnityPy third_party/Grasscutter third_party/LunarCore third_party/godot-demo-projects ;;
  UnityPy|Grasscutter|LunarCore|godot-demo-projects) git submodule update --init -- "third_party/${1:-UnityPy}" ;;
  *) echo 'Usage: scripts/setup-upstreams.sh {UnityPy|Grasscutter|LunarCore|godot-demo-projects|all}' >&2; exit 2 ;;
esac
