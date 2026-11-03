#!/usr/bin/env python3
"""Repository guard.

Four checks that matter for a documentation repository whose whole premise is
"we describe the format, we do not distribute the game":

1. No file type that must never be committed (container payloads, indexes,
   game dumps, keys, saves, certs).
2. No oversized file (a specification is text; anything above 5 MB is not).
3. No secret-shaped string and no absolute local path in any text file.
4. Every relative Markdown link resolves, and every document has a title.

Deliberately not a prose linter. Line length and table alignment are taste;
shipping a 247 MB payload or a `C:\\\\Users\\\\...` path is not.

Exit code 0 when clean, 1 when something fails. Usable locally and in CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAX_BYTES = 5 * 1024 * 1024

FORBIDDEN_SUFFIXES = {
    # Pokopia containers and indexes
    ".bin", ".idx",
    # Switch container formats and decrypted output
    ".nsp", ".xci", ".nca", ".ncz", ".nsz", ".xcz", ".romfs", ".exefs",
    ".npdm", ".nso", ".nro", ".kip", ".kipx", ".tik",
    # Keys, certificates, saves
    ".keys", ".pem", ".p12", ".pfx", ".key", ".crt", ".sav",
}

FORBIDDEN_NAMES = {
    "prod.keys", "title.keys", "console.keys", "keys.txt", "profiles.dat",
}

# Shapes of things that leak. Kept narrow on purpose: a false positive here
# wastes a maintainer's time, a false negative ships a secret.
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"), "GitHub fine-grained token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"), "GitLab token"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "Slack token"),
]

# A documentation repository must not leak the machine it was written on.
LOCAL_PATH_PATTERNS = [
    (re.compile(r"[A-Za-z]:\\Users\\"), "absolute Windows user path"),
    (re.compile(r"[A-Za-z]:\\Proyectos\\"), "absolute Windows project path"),
    (re.compile(r"/home/[a-z0-9_-]+/"), "absolute POSIX home path"),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".cache"}

TEXT_SUFFIXES = {".md", ".txt", ".yml", ".yaml", ".json", ".py", ".sh", "", ".gitignore", ".gitattributes"}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def iter_files() -> list[Path]:
    out: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        out.append(path)
    return out


def check_forbidden(files: list[Path], errors: list[str]) -> None:
    for path in files:
        rel = path.relative_to(ROOT)
        if path.name.lower() == "license":
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES or path.name.lower() in FORBIDDEN_NAMES:
            errors.append(f"forbidden file committed: {rel}")


def check_size(files: list[Path], errors: list[str]) -> None:
    for path in files:
        size = path.stat().st_size
        if size > MAX_BYTES:
            errors.append(
                f"file too large ({size / 1024 / 1024:.1f} MB > 5 MB): {path.relative_to(ROOT)}"
            )


def check_text_rules(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".gitignore", ".gitattributes"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern, label in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"possible {label} at {path.relative_to(ROOT)}:{line}")
        for pattern, label in LOCAL_PATH_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{label} at {path.relative_to(ROOT)}:{line}")


def check_links(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8", errors="ignore")

        if not text.lstrip().startswith("#"):
            errors.append(f"no leading title heading: {rel}")

        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                continue
            if target.startswith("#"):
                continue
            clean = target.split("#")[0].split("?")[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                line = text.count("\n", 0, text.find(target)) + 1
                errors.append(f"broken relative link in {rel}:{line} -> {target}")


def main() -> int:
    files = iter_files()
    errors: list[str] = []

    check_forbidden(files, errors)
    check_size(files, errors)
    check_text_rules(files, errors)
    check_links(files, errors)

    if errors:
        print(f"FAIL — {len(errors)} problem(s):\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"OK — {len(files)} files checked: no forbidden material, no file over 5 MB, "
        "no secrets, no local paths, links resolve."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
