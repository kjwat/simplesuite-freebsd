#!/usr/bin/env python3
"""Validate the complete native source receipt before Scriptorium builds it."""
import hashlib
import json
from pathlib import Path
import re
import sys


def verify(root):
    receipt = json.loads((root / '.simpleos-freebsd-source.json').read_text())
    if (receipt.get('format') != 1 or receipt.get('target') != 'FreeBSD-15-amd64'
            or not re.fullmatch('[0-9a-f]{40}', receipt.get('upstream_revision', ''))
            or not isinstance(receipt.get('files'), dict) or not receipt['files']):
        raise ValueError('Invalid native SimpleSuite source receipt')
    actual = {str(path.relative_to(root)) for path in root.rglob('*') if path.is_file()
              and path.name != '.simpleos-freebsd-source.json'
              and not any(part in {'.git', 'build', '__pycache__'} or part.startswith(('build-', 'build_'))
                          for part in path.relative_to(root).parts[:-1])}
    if actual != set(receipt['files']):
        raise ValueError('Native source file list differs from its port receipt')
    for name, digest in receipt['files'].items():
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or str(path) != name:
            raise ValueError('Unsafe source receipt path: ' + name)
        source = root / path
        if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
            raise ValueError('Native source contains an unexpected link: ' + name)
        if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
            raise ValueError('Native source changed since port preparation: ' + name)
    return receipt['upstream_revision']


if __name__ == '__main__':
    try:
        print(verify(Path(sys.argv[1])))
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(str(error))
