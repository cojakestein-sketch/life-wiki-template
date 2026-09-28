#!/usr/bin/env python3
"""Fail if this repository is about to share something its privacy labels forbid.

Checks, using only the standard library:
  1. Tracked Markdown files labelled `privacy: local-only` or `privacy: never-store`.
  2. Untracked `local-only` files that .gitignore does not cover (a label alone
     protects nothing; `git add .` would commit them).
  3. Maintained pages (see MAINTAINED_DIRS) without privacy/updated/sources frontmatter.
  4. Common secret formats in tracked text files.

Tracked content is read from the Git index, so a pre-commit hook checks exactly what
is about to be committed. Exit code 1 means at least one problem was found.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

MAINTAINED_DIRS = ("me/", "areas/")
REQUIRED_FIELDS = ("privacy", "updated", "sources")
NAVIGATION_FILES = {"index.md", "README.md"}
BLOCKED_TRACKED = {"local-only", "never-store"}

SECRET_PATTERNS = {
    "private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "Anthropic API key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    "OpenAI-style API key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
}


def git(*args: str, stdin: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args], input=stdin, capture_output=True, check=True
    ).stdout


def frontmatter(text: str) -> dict[str, str]:
    """Top-level `key: value` pairs from a leading --- block (no YAML dependency)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return {}  # unterminated block: treat as no frontmatter


def tracked_files() -> dict[str, bytes]:
    """Path -> content for every file in the index."""
    entries = git("ls-files", "-s", "-z").split(b"\0")
    paths, shas = [], []
    for entry in filter(None, entries):
        meta, path = entry.split(b"\t", 1)
        mode, sha, _stage = meta.split(b" ")
        if mode == b"160000":  # submodule
            continue
        paths.append(path.decode())
        shas.append(sha)
    if not shas:
        return {}
    out = git("cat-file", "--batch", stdin=b"\n".join(shas) + b"\n")
    contents: dict[str, bytes] = {}
    pos = 0
    for path in paths:
        header_end = out.index(b"\n", pos)
        size = int(out[pos:header_end].split(b" ")[2])
        start = header_end + 1
        contents[path] = out[start : start + size]
        pos = start + size + 1
    return contents


def check(repo_root: Path) -> list[str]:
    problems: list[str] = []
    tracked = tracked_files()

    for path, blob in tracked.items():
        if b"\0" in blob[:8000]:
            continue  # binary
        text = blob.decode("utf-8", errors="replace")

        if path.endswith(".md"):
            fields = frontmatter(text)
            level = fields.get("privacy", "")
            if level in BLOCKED_TRACKED:
                problems.append(f"{path}: tracked but labelled privacy: {level}")
            if path.startswith(MAINTAINED_DIRS) and Path(path).name not in NAVIGATION_FILES:
                missing = [f for f in REQUIRED_FIELDS if f not in fields]
                if missing:
                    problems.append(f"{path}: missing frontmatter {', '.join(missing)}")

        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                problems.append(f"{path}: looks like it contains a {label}")

    untracked = git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
    for raw_path in filter(None, untracked):
        path = raw_path.decode()
        if not path.endswith(".md"):
            continue
        try:
            text = (repo_root / path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if frontmatter(text).get("privacy") == "local-only":
            problems.append(f"{path}: labelled local-only but not covered by .gitignore")

    return problems


def main() -> int:
    try:
        root = Path(git("rev-parse", "--show-toplevel").decode().strip())
    except subprocess.CalledProcessError:
        print("check_privacy: not inside a Git repository", file=sys.stderr)
        return 2
    os.chdir(root)  # git reports untracked paths relative to the working directory
    problems = check(root)
    if problems:
        print("Privacy check failed:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Privacy check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
