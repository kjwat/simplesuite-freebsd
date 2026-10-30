# Native FreeBSD SimpleSuite

This is the separate FreeBSD 15.x amd64 upstream. Linux and macOS use
https://github.com/kjwat/simplesuite. This checkout refuses to build on another OS.

The full port remains in progress. SimpleTerm, SimplePDF and the terminal suite
have reached native compilation; the complete release gate and application
runtime acceptance remain pending. Bluetooth, the complete SimpleVol audio
graph, device integration and the complete preinstalled desktop are unfinished.
Do not interpret a public source repository as a finished SimpleOS image.

Run `./build.sh` as your normal user, with administrator authentication available
for dependencies and installation. GNU make is `gmake` on FreeBSD. The complete
desktop interface remains `gmake full` and `gmake DESTDIR=/absolute/stage install-full`.
Run `gmake test-full` and `gmake release-simplewords` before accepting a release.
No applications are installed in `~/.local/bin`.

The SID synthesizer deliberately uses native libsidplayfp **2.12.0**, matching
the Linux reference API, instead of changing synthesis behavior for the 3.x API.
`freebsd/bootstrap.sh` builds it from the bundled source archive, validates
SHA256 `bc4f4fa203dcf0736fe48c23dce9aa0db825370e5941e7595e4851efe6937cdc`,
and installs it under `/usr/local/lib/simpleos/libsidplayfp-2.12.0`.
The archive comes from Debian's official source pool:
https://deb.debian.org/debian/pool/main/libs/libsidplayfp/libsidplayfp_2.12.0.orig.tar.gz.
System libsidplayfp packages are retained. Staged builds keep dependencies staged.

The initial source adaptation is based on Linux SimpleSuite revision
`3011083a7a36b1c1126ddaee512ef8cbd1f7ce40`. The native receipt records the
complete adapted source hashes for installations from a captured source tree.
A normal Git checkout also retains the clean-commit release gate.

Samba uses the native `samba_server` service and `/usr/local/etc/smb4.conf`.
Its transactional adapter has fixture coverage; physical LAN/iOS acceptance is
still required. No personal credentials or user data are included.
