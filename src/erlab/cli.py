"""Command line interface for read-only, offline research."""
import argparse
import json
from pathlib import Path
import sys

from .formats import identify_file
from .inventory import scan_directory, summarize, diff_scans, write_json, load_json


def profiles_dir() -> Path:
    # Sources run from editable install OR standard source checkout.
    return Path(__file__).resolve().parents[2] / "games"


def list_games(folder: Path) -> list[dict]:
    games = []
    if not folder.is_dir():
        return games
    for p in sorted(folder.glob("*/profile.json")):
        if p.parent.name.startswith("_"):
            continue
        try:
            data = load_json(p)
            if isinstance(data, dict) and data.get("id"):
                games.append({"id": data["id"], "name": data.get("name", data["id"]), "status": data.get("status", "unknown")})
        except (ValueError, OSError, json.JSONDecodeError):
            continue
    return games


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="erlab", description="二次元游戏离线资源分析工具 / read-only offline inventory")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("games", help="List registered game research profiles")
    inspect_p = sub.add_parser("inspect", help="Detect a local file's format by magic bytes")
    inspect_p.add_argument("file", type=Path)
    scan_p = sub.add_parser("scan", help="Scan directory and generate an inventory JSON")
    scan_p.add_argument("folder", type=Path)
    scan_p.add_argument("--out", required=True, type=Path)
    sum_p = sub.add_parser("summary", help="Summarize inventory JSON")
    sum_p.add_argument("inventory", type=Path)
    diff_p = sub.add_parser("diff", help="Compare two scan snapshots")
    diff_p.add_argument("before", type=Path)
    diff_p.add_argument("after", type=Path)
    diff_p.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.action == "games":
            result = list_games(profiles_dir())
        elif args.action == "inspect":
            result = {"path": str(args.file), **identify_file(args.file)}
        elif args.action == "scan":
            # Reject output inside source folder to avoid self-inclusion in future scans.
            if args.out.resolve().is_relative_to(args.folder.resolve()):
                raise ValueError("Output must be outside the directory being scanned")
            result = scan_directory(args.folder)
            write_json(result, args.out)
            print(f"Wrote inventory to {args.out}", file=sys.stderr)
            result = summarize(result)
        elif args.action == "summary":
            result = summarize(load_json(args.inventory))
        else:
            result = diff_scans(load_json(args.before), load_json(args.after))
            if args.out:
                write_json(result, args.out)
                print(f"Wrote diff to {args.out}", file=sys.stderr)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
