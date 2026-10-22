"""Read-only Unity asset indexing/export through the EXISTING UnityPy project.

Upstream: https://github.com/K0lb3/UnityPy (MIT).
No decompression, encrypted-game bypass or decryption code is implemented here.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SUPPORTED_EXPORTS = frozenset({'Texture2D', 'Sprite', 'TextAsset'})


def _unitypy():
    try:
        import UnityPy  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError('缺少 UnityPy。请执行: python -m pip install -e ".[unity]"') from exc
    return UnityPy


def _name(value: object) -> str:
    """Prevent asset-provided names from escaping the designated export folder."""
    raw = str(value or 'unnamed').replace('\\', '/').split('/')[-1]
    cleaned = re.sub(r'[^\w.\- ]', '_', raw, flags=re.UNICODE).strip(' .')
    return cleaned[:100] if cleaned and cleaned not in {'.', '..'} else 'unnamed'


def _objects(src: Path):
    if not src.is_file():
        raise ValueError(f'Not an existing file: {src}')
    env = _unitypy().load(str(src))
    yield from env.objects


def inspect(src: Path, types: set[str] | None = None, limit: int = 10000) -> dict:
    """Enumerate object metadata without eagerly decoding objects."""
    if limit < 1:
        raise ValueError('limit must be >= 1')
    items = []
    counts: dict[str, int] = {}
    truncated = False
    for obj in _objects(src):
        kind = str(obj.type.name)
        if types and kind not in types:
            continue
        if len(items) >= limit:
            truncated = True
            break
        counts[kind] = counts.get(kind, 0) + 1
        items.append({'path_id': str(getattr(obj, 'path_id', '')), 'type': kind})
    return {'source': str(src), 'objects': items, 'counts': counts, 'truncated': truncated,
            'parser': 'K0lb3/UnityPy (external MIT dependency)'}


def export(src: Path, out_dir: Path, types: set[str] | None = None,
           limit: int = 1000) -> dict:
    """Export selected readable assets. No original source data is modified."""
    if limit < 1:
        raise ValueError('limit must be >= 1')
    if types and not types <= SUPPORTED_EXPORTS:
        raise ValueError(f'Export supports only {sorted(SUPPORTED_EXPORTS)}')
    allowed = types or SUPPORTED_EXPORTS
    files = []
    errors = []
    for obj in _objects(src):
        kind = str(obj.type.name)
        if kind not in allowed:
            continue
        if len(files) >= limit:
            break
        try:
            data = obj.parse_as_object()
            stem = _name(getattr(data, 'm_Name', None) or getattr(obj, 'path_id', None))
            stable_id = _name(str(getattr(obj, 'path_id', len(files))))
            folder = out_dir / kind
            folder.mkdir(parents=True, exist_ok=True)
            if kind in {'Texture2D', 'Sprite'}:
                target = folder / f'{stem}_{stable_id}.png'
                data.image.save(target)
            elif kind == 'TextAsset':
                target = folder / f'{stem}_{stable_id}.bytes'
                script = data.m_Script
                target.write_bytes(script.encode('utf-8') if isinstance(script, str) else bytes(script))
            else:
                continue
            files.append(str(target))
        except (AttributeError, ValueError, TypeError, OSError, RuntimeError) as exc:
            errors.append({'path_id': str(getattr(obj, 'path_id', '')), 'error': str(exc)})
    return {'source': str(src), 'out': str(out_dir), 'exported': files, 'errors': errors}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog='erlab-unity', description='调用现有 UnityPy 对本地 Unity 文件进行只读研究')
    subs = p.add_subparsers(dest='cmd', required=True)
    for cmd in ('inspect', 'export'):
        sub = subs.add_parser(cmd)
        sub.add_argument('source', type=Path)
        sub.add_argument('--types', help='逗号分隔，例如 Texture2D,Sprite,TextAsset')
        sub.add_argument('--limit', type=int, default=1000)
        if cmd == 'export':
            sub.add_argument('--out', required=True, type=Path)
    args = p.parse_args(argv)
    types = set(filter(None, (v.strip() for v in args.types.split(',')))) if args.types else None
    try:
        if args.cmd == 'inspect':
            result = inspect(args.source, types=types, limit=args.limit)
        else:
            result = export(args.source, args.out, types=types, limit=args.limit)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if not result.get('errors') else 1
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
