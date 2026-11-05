#!/usr/bin/env python3
"""Launch official Obsidian argv supplied as JSON on stdin. No workflow decisions."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

SANITIZE = ('unset __CFBundleIdentifier LaunchInstanceID XPC_SERVICE_NAME '
            'CODEX_CI CODEX_SANDBOX CODEX_SHELL; export TERM=xterm-256color; ')


def command(argv, platform=sys.platform, environ=None):
    if not isinstance(argv, list) or not argv or any(
        not isinstance(arg, str) or '\0' in arg for arg in argv
    ):
        raise ValueError('argv must be a nonempty JSON array of NUL-free strings')
    if platform != 'darwin':
        return ['obsidian', *argv]
    env = os.environ if environ is None else environ
    shell = env.get('CODEX_OBSIDIAN_ZSH_PATH') or '/usr/local/bin/zsh'
    if not Path(shell).is_absolute() or not os.access(shell, os.X_OK):
        raise ValueError('Set CODEX_OBSIDIAN_ZSH_PATH to an absolute executable Zsh path '
                         '(for example /bin/zsh), then retry the read-only probe')
    # shlex.join quotes every untrusted argument, including embedded apostrophes.
    return ['script', '-q', '/dev/null', shell, '-ilc',
            SANITIZE + shlex.join(['obsidian', *argv])]


def content_argument(text):
    """Encode only the documented CLI newline/tab sequences; reject ambiguity."""
    if not isinstance(text, str) or '\0' in text or '\r' in text:
        raise ValueError('content must be NUL-free LF text; CR/CRLF transport is unverified')
    if '\\n' in text or '\\t' in text:
        raise ValueError('literal backslash-n/backslash-t transport is unverified; do not write')
    return 'content=' + text.replace('\n', '\\n').replace('\t', '\\t')


def main():
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict) or set(request) - {'argv', 'content'}:
            raise ValueError('expected {"argv": [...], "content": optional literal text}')
        argv = request.get('argv')
        if not isinstance(argv, list) or not argv:
            raise ValueError('argv must include the requested CLI command')
        if 'content' in request:
            if not isinstance(argv, list) or any(
                isinstance(a, str) and a.startswith('content=') for a in argv
            ):
                raise ValueError('provide content once, separately from argv')
            argv = [*argv, content_argument(request['content'])]
        launch = command(argv)
        result = subprocess.run(launch, capture_output=True, timeout=30)
        report = {'status': 'process-completed', 'returncode': result.returncode,
                  'stdout': result.stdout.decode('utf-8', errors='replace'),
                  'stderr': result.stderr.decode('utf-8', errors='replace')}
        # A zero exit from Obsidian or script is not evidence of a completed write.
        print(json.dumps(report, ensure_ascii=False))
        return 0 if result.returncode == 0 else 1
    except subprocess.TimeoutExpired as error:
        print(json.dumps({'status': 'uncertain', 'error': '30-second timeout; inspect state and establish original completion before retry',
                          'stdout': (error.stdout or b'').decode('utf-8', errors='replace'),
                          'stderr': (error.stderr or b'').decode('utf-8', errors='replace')}))
        return 2
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({'status': 'launch-failed', 'error': str(error)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
