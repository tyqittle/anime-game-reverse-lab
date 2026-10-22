"""Stage-0, read-only Android APK feasibility inventory.

Findings are filename/DEX-string *hints*, not proof of supported engine,
working network endpoints, encryption or a compatible local server.
No APK modification, extraction of copyrighted assets, or network contact.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

URL_HOST = re.compile(rb'https?://([a-z0-9-]+(?:\.[a-z0-9-]+)+)', flags=re.IGNORECASE)
MAX_FILES = 40000
MAX_UNPACKED = 8 * 1024**3
MAX_TOTAL_STRINGS = 80 * 1024**2

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024**2), b""):
            h.update(chunk)
    return h.hexdigest()

def inspect(apk: Path) -> dict:
    if not apk.is_file() or apk.suffix.lower() != ".apk":
        raise ValueError("Provide an existing Android .apk.")
    if apk.stat().st_size > 2 * 1024**3:
        raise ValueError("APK too large for the bounded scanner.")
    if not zipfile.is_zipfile(apk):
        raise ValueError("Invalid ZIP-format APK.")
    with zipfile.ZipFile(apk) as z:
        entries = z.infolist()
        if len(entries) > MAX_FILES or sum(f.file_size for f in entries) > MAX_UNPACKED:
            raise ValueError("Archive exceeds safety limits.")
        names = {f.filename.lower() for f in entries}
        engines = {}
        signals = {
            "Unity": ["libunity.so", "libil2cpp.so", "assets/bin/data/"],
            "Unreal": ["libue4.so", "libunreal.so", ".pak", ".ucas", ".utoc"],
            "Cocos2d-x": ["libcocos2d", "libcocos.so"],
            "Godot": ["libgodot_android.so", "assets/.godot", "assets/project.binary"],
            "Flutter": ["libflutter.so", "assets/flutter_assets/"]
        }
        for engine, patterns in signals.items():
            found = [p for p in patterns if any(p in name for name in names)]
            if found:
                engines[engine] = sorted(found)
        network_sdks = set()
        hosts = set()
        remaining = MAX_TOTAL_STRINGS
        for info in entries:
            entry_name = Path(info.filename).name.lower()
            if not (re.fullmatch(r'classes\d*\.dex', entry_name) or
                    entry_name.endswith((".json", ".properties", ".txt", ".xml", ".cfg"))):
                continue
            if not 0 < info.file_size <= 16*1024**2 or info.file_size > remaining:
                continue
            remaining -= info.file_size
            chunk = z.read(info)
            lowered = chunk.lower()
            for token in (b"okhttp", b"retrofit", b"unitywebrequest",
                          b"volley", b"grpc", b"websocket", b"ktor"):
                if token in lowered:
                    network_sdks.add(token.decode("ascii"))
            for match in URL_HOST.finditer(chunk):
                host = match.group(1).decode("ascii", "ignore").lower()
                if len(host) <= 253:
                    hosts.add(host)  # Never save URL query strings or secrets.
                if len(hosts) >= 200:
                    break
        signatures = sorted(p for p in names if p.startswith("meta-inf/") and
                            p.endswith((".rsa", ".sf", ".dsa", ".ec")))
        native = sorted(p for p in names if p.endswith(".so"))
        packer_hints = sorted({Path(p).name for p in native if
                              any(x in p for x in ("jiagu", "dexprotector", "libprotect"))})
        return {
            "stage": 0, "apk_filename": apk.name, "sha256": sha256(apk),
            "size": apk.stat().st_size, "zip_entries": len(entries),
            "manifest_present": "androidmanifest.xml" in names,
            "engine_hints_not_verified": engines,
            "native_library_count": len(native),
            "network_sdk_string_hints": sorted(network_sdks),
            "candidate_http_hosts_not_verified": sorted(hosts),
            "legacy_signature_entries": signatures[:20],
            "packer_name_hints_not_verified": packer_hints,
            "ssl_pinning": "unknown", "encryption": "unknown",
            "actual_protocol": "unknown", "server_availability": "unknown",
            "offline_feasibility": "unassessed: requires runtime and game context",
            "warning": ("Read-only heuristic inventory. Host strings may belong to "
                        "advertising or unused code. No packet capture or bypass was performed.")
        }

def report(data: dict) -> str:
    return (
        "# APK 阶段 0：只读可行性报告\n\n"
        + "- 文件 SHA-256：" + data["sha256"] + "\n"
        + "- 引擎线索：" + json.dumps(data["engine_hints_not_verified"], ensure_ascii=False) + "\n"
        + "- 网络 SDK 字符串：" + ", ".join(data["network_sdk_string_hints"]) + "\n"
        + "- 候选域名（不含路径、口令）："
        + ", ".join(data["candidate_http_hosts_not_verified"]) + "\n"
        + "- 加密/SSL Pinning/服务端兼容性：**未验证**\n\n"
        + "静态线索不等于游戏可离线运行；后续必须使用获授权的客户端副本"
        + "与隔离测试环境验证游戏登录、协议、核心玩法和本地存档。\n"
    )

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Read-only, non-network Android APK inspection")
    p.add_argument("apk", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--markdown", type=Path)
    args = p.parse_args(argv)
    try:
        result = inspect(args.apk)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
        if args.markdown:
            args.markdown.parent.mkdir(parents=True, exist_ok=True)
            args.markdown.write_text(report(result), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as e:
        print(f"APK scan failed: {e}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
