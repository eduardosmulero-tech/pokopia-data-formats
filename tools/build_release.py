#!/usr/bin/env python3
"""Build the release artifact for this repository.

A release of a documentation repository is a tarball of the tracked tree plus a
`SHA256SUMS` file beside it: two downloads, one `sha256sum -c`, and the reader
knows the bytes match the tag they came from.

The archive is deterministic on purpose — sorted names, fixed mtime, no owner
names, gzip with mtime 0 — so building it twice from the same commit gives the
same sha256. `git archive` is deliberately not used: GitHub's source zips are
generated on demand and their compression is not reproducible (see
PROTOCOLO-PUBLICACION-GIT.md §8).

Usage:
    python tools/build_release.py [--version X.Y.Z] [--out DIR]

Exit code 0 on success, 1 on a dirty tree or a missing version.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "pokopia-data-formats"
MTIME = 1700000000  # fixed: 2023-11-14T22:13:20Z, inside the tar header only


def git(*args: str) -> str:
    out = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return out.stdout.strip()


def version_from_git() -> str:
    tags = git("tag", "--points-at", "HEAD").splitlines()
    for tag in tags:
        if tag.startswith("v"):
            return tag[1:]
    raise SystemExit("no vX.Y.Z tag points at HEAD; pass --version")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version")
    parser.add_argument("--out", default=str(ROOT / "build" / "release"))
    args = parser.parse_args()

    if git("status", "--porcelain"):
        print("refusing to build from a dirty tree: commit first", file=sys.stderr)
        return 1

    version = args.version or version_from_git()
    files = [f for f in git("ls-files").splitlines() if f]
    if not files:
        print("no tracked files", file=sys.stderr)
        return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"{PREFIX}-v{version}.tar.gz"
    tar_path = out_dir / name

    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for rel in sorted(files):
            data = (ROOT / rel).read_bytes()
            info = tarfile.TarInfo(f"{PREFIX}-{version}/{rel}")
            info.size = len(data)
            info.mtime = MTIME
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))

    # gzip with mtime 0 and no filename: the header stops depending on when it ran.
    tar_path.write_bytes(_gzip(buffer.getvalue()))

    digest = hashlib.sha256(tar_path.read_bytes()).hexdigest()
    sums = out_dir / "SHA256SUMS"
    sums.write_text(f"{digest}  {name}\n", encoding="utf-8")

    print(f"{name}  {len(buffer.getvalue())} B uncompressed")
    print(f"sha256 {digest}")
    print(f"wrote {tar_path} and {sums}")
    print(f"files in the archive: {len(files)}")
    return 0


def _gzip(payload: bytes) -> bytes:
    import gzip

    raw = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as gz:
        gz.write(payload)
    return raw.getvalue()


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(main())
