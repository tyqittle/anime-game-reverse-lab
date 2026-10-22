"""Local-only scan and diff with deterministic relative paths and hashes."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

from .formats import identify_file

SCHEMA_VERSION = 1


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def scan_directory(folder: Path) -> dict:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        raise ValueError(f"Not a directory: {folder}")
    files = []
    errors = []
    # Using Path.rglob only follows the source directory; skip symlinked files and folders.
    for path in sorted(folder.rglob("*"), key=lambda p: p.as_posix().casefold()):
        rel = path.relative_to(folder).as_posix()
        try:
            if path.is_symlink() or not path.is_file():
                continue
            stat = path.stat()
            fmt = identify_file(path)
            files.append({
                "path": rel,
                "size": stat.st_size,
                "sha256": sha256_file(path),
                "extension": path.suffix.lower(),
                **fmt,
            })
        except (OSError, PermissionError) as exc:
            errors.append({"path": rel, "error": type(exc).__name__})
    return {
        "schema_version": SCHEMA_VERSION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_name": folder.name,
        "files": files,
        "errors": errors,
    }


def summarize(scan: dict) -> dict:
    files = scan.get("files", [])
    return {
        "total_files": len(files),
        "total_bytes": sum(e["size"] for e in files),
        "format_counts": dict(sorted(Counter(e["format"] for e in files).items())),
        "extensions": dict(sorted(Counter(e["extension"] or "(none)" for e in files).items())),
        "duplicate_sha256_groups": sum(c > 1 for c in Counter(e["sha256"] for e in files).values()),
        "scan_errors": len(scan.get("errors", [])),
    }


def diff_scans(before: dict, after: dict) -> dict:
    old = {f["path"]: f for f in before["files"]}
    new = {f["path"]: f for f in after["files"]}
    old_paths, new_paths = set(old), set(new)
    return {
        "added": sorted(new_paths - old_paths),
        "removed": sorted(old_paths - new_paths),
        "modified": sorted(p for p in old_paths & new_paths if old[p]["sha256"] != new[p]["sha256"]),
        "unchanged_count": sum(old[p]["sha256"] == new[p]["sha256"] for p in old_paths & new_paths),
    }


def write_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False, indent=2, sort_keys=True)
        out.write("\n")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
