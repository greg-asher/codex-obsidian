#!/usr/bin/env python3
"""Pure exact-text preview and state checks. Never writes notes or launches commands."""
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def preview(before, old, new):
    if not all(isinstance(value, str) for value in (before, old, new)):
        raise ValueError('before, old, new must be literal UTF-8 text')
    if not old or before.find(old) < 0 or before.find(old, before.find(old) + 1) >= 0:
        raise ValueError('old must match exactly once; resolve the target with more context')
    start = before.index(old)
    after = before[:start] + new + before[start + len(old):]
    lines = difflib.unified_diff(before.splitlines(keepends=True),
                                 after.splitlines(keepends=True),
                                 fromfile='before', tofile='proposed')
    diff = ''.join(line if line.endswith('\n') else
                   line + '\n\\ No newline at end of file\n' for line in lines)
    return {'before_sha256': digest(before), 'after_sha256': digest(after),
            'content': after, 'diff': diff}


def state(current, before, expected):
    """None means proven absent, never an unreadable/failed CLI response."""
    if current == expected:
        return 'already-applied'
    if current == before:
        return 'ready'
    return 'conflict'


def contained_target(root, relative):
    vault = Path(root)
    path = PurePosixPath(relative)
    if (not vault.is_absolute() or not vault.is_dir() or not relative
            or path.is_absolute() or '\\' in relative or ':' in relative
            or any(part in ('', '.', '..') for part in relative.split('/'))):
        raise ValueError('require existing absolute vault root and exact vault-relative path')
    vault = vault.resolve()
    target = vault.joinpath(*path.parts).resolve()
    if not target.is_relative_to(vault) or target == vault:
        raise ValueError('target escapes the resolved vault root (including symlinks)')
    return target


def main():
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict) or set(request) != {'before', 'old', 'new'}:
            raise ValueError('expected exactly {"before": text, "old": text, "new": text}')
        print(json.dumps(preview(**request), ensure_ascii=False))
        return 0
    except (ValueError, TypeError, UnicodeError) as error:
        print(json.dumps({'status': 'blocked', 'error': str(error)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
