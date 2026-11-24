#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261123 entry.

The finished image lives in this repository as entry.png. This program
copies those exact bytes to entry.png inside the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (or /output when it is unset)
and exits 0. Python standard library only; it makes no network calls
and reads nothing outside this repository.
"""

import os
import sys


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, "entry.png")
    if not os.path.isfile(source):
        sys.stderr.write("entry.png is missing next to main.py\n")
        return 1
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    with open(source, "rb") as handle:
        payload = handle.read()
    with open(os.path.join(target_dir, "entry.png"), "wb") as handle:
        handle.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
