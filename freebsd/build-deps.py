#!/usr/bin/env python3
"""Build the native SID reference ABI into a disposable stage for installation."""
import argparse
import hashlib
import os
from pathlib import Path
import platform
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '/usr/local/lib/simpleos/libsidplayfp-2.12.0'
SHA = 'bc4f4fa203dcf0736fe48c23dce9aa0db825370e5941e7595e4851efe6937cdc'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', required=True, type=Path)
    args = parser.parse_args()
    if platform.system() != 'FreeBSD':
        raise SystemExit('Native FreeBSD dependencies only')
    archive = ROOT / 'distfiles/libsidplayfp_2.12.0.orig.tar.gz'
    if hashlib.sha256(archive.read_bytes()).hexdigest() != SHA:
        raise SystemExit('SID source checksum failed')
    work = ROOT / 'build/freebsd-deps'
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'libsidplayfp-2.12.0'
    if not source.exists():
        with tarfile.open(archive) as tar:
            tar.extractall(work, filter='data')
    if not (source / 'Makefile').exists():
        subprocess.run(['./configure', '--prefix=' + PREFIX, '--disable-static',
                        '--disable-hardsid', '--without-exsid'], cwd=source, check=True)
    subprocess.run(['gmake', '-j2'], cwd=source, check=True)
    subprocess.run(['gmake', 'install', 'DESTDIR=' + str(args.stage.resolve())], cwd=source, check=True)
    installed = args.stage.resolve() / PREFIX.lstrip('/')
    (installed / '.simpleos-source-sha256').write_text(SHA + '\n')
    pcdir = work / 'pkgconfig'
    pcdir.mkdir(exist_ok=True)
    pc = installed / 'lib/pkgconfig/libsidplayfp.pc'
    (pcdir / pc.name).write_text(pc.read_text().replace('prefix=' + PREFIX, 'prefix=' + str(installed)))


if __name__ == '__main__':
    main()
