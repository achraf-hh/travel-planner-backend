#!/usr/bin/env python3
"""
Helper script that keeps VERSION and pyproject.toml in sync.
Usage:
  python scripts/bump_version.py show
  python scripts/bump_version.py bump [major|minor|patch]
  python scripts/bump_version.py set 1.2.3
"""

from __future__ import annotations

import argparse
import pathlib
import re
from typing import Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
PYPROJECT_FILE = ROOT / "pyproject.toml"
VERSION_PATTERN = re.compile(r'version\s*=\s*"(?P<version>\d+\.\d+\.\d+)"')


def read_version() -> Tuple[int, int, int]:
    version_text = VERSION_FILE.read_text().strip()
    major, minor, patch = (int(part) for part in version_text.split("."))
    return major, minor, patch


def write_version(version: str) -> None:
    VERSION_FILE.write_text(f"{version}\n")
    update_pyproject(version)


def update_pyproject(version: str) -> None:
    text = PYPROJECT_FILE.read_text()
    new_text, count = VERSION_PATTERN.subn(f'version = "{version}"', text, count=1)
    if count != 1:
        raise RuntimeError("Could not locate project version in pyproject.toml")
    PYPROJECT_FILE.write_text(new_text)


def bump(part: str) -> str:
    major, minor, patch = read_version()
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def set_version(explicit_version: str) -> str:
    if not re.fullmatch(r"\d+\.\d+\.\d+", explicit_version):
        raise ValueError("Version must be in MAJOR.MINOR.PATCH format")
    write_version(explicit_version)
    return explicit_version


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage project version metadata.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show", help="Print the current semantic version.")

    bump_parser = subparsers.add_parser("bump", help="Increment the semantic version.")
    bump_parser.add_argument("part", choices=["major", "minor", "patch"])

    set_parser = subparsers.add_parser("set", help="Set an explicit semantic version.")
    set_parser.add_argument("value", help="Desired version (MAJOR.MINOR.PATCH)")

    args = parser.parse_args()

    if args.command == "show":
        print(".".join(str(part) for part in read_version()))
        return

    if args.command == "bump":
        new_version = bump(args.part)
        write_version(new_version)
        print(new_version)
        return

    if args.command == "set":
        new_version = set_version(args.value)
        print(new_version)


if __name__ == "__main__":
    main()

