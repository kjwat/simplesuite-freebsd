# Sourced by the native suite installers; simpleos_suite_root is their source tree.
simpleos_sid_prefix=/usr/local/lib/simpleos/libsidplayfp-2.12.0
simpleos_sid_sha=bc4f4fa203dcf0736fe48c23dce9aa0db825370e5941e7595e4851efe6937cdc
if [ "$(cat "$simpleos_sid_prefix/.simpleos-source-sha256" 2>/dev/null || true)" != "$simpleos_sid_sha" ]; then
    simpleos_sid_stage=$simpleos_suite_root/build/freebsd-deps-stage
    python3 "$simpleos_suite_root/freebsd/build-deps.py" --stage "$simpleos_sid_stage" || exit $?
    if [ -z "${DESTDIR:-}" ]; then
        simpleos_deps_root() {
            if [ "$(id -u)" = 0 ]; then "$@"
            elif command -v sudo >/dev/null 2>&1; then sudo "$@"
            elif command -v doas >/dev/null 2>&1; then doas "$@"
            else echo 'Administrator authentication is required for native libraries.' >&2; return 1; fi
        }
        simpleos_deps_root mkdir -p /usr/local/lib/simpleos || exit $?
        simpleos_deps_root cp -Rp "$simpleos_sid_stage$simpleos_sid_prefix" /usr/local/lib/simpleos/ || exit $?
    fi
    PKG_CONFIG_PATH=$simpleos_suite_root/build/freebsd-deps/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}
    LD_LIBRARY_PATH=$simpleos_sid_stage$simpleos_sid_prefix/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
else
    PKG_CONFIG_PATH=$simpleos_sid_prefix/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}
    LD_LIBRARY_PATH=$simpleos_sid_prefix/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
fi
LDFLAGS="${LDFLAGS:-} -Wl,-rpath,$simpleos_sid_prefix/lib"
export PKG_CONFIG_PATH LD_LIBRARY_PATH LDFLAGS
