#!/usr/bin/env python3
"""File organizer: sort files into subfolders by extension."""

import argparse
# NEW: pathlib.Path gives us an OS-independent way to work with filesystem paths.
# It replaces messy string operations like os.path.join() with clean dot-notation.
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Organize files by extension."
    )
    parser.add_argument(
        "directory",
        help="Path to the directory you want to organize"
    )
    args = parser.parse_args()

    # NEW: Convert the raw string the user typed into a Path object.
    # .resolve() turns relative paths ("../docs") into absolute ones ("/home/user/docs")
    # so there's never any ambiguity about where we're working.
    target = Path(args.directory).resolve()

    # NEW: Validate before doing any work.
    # .is_dir() returns True only if the path exists AND is a directory (not a file).
    # Printing an error and returning early is called a "guard clause" —
    # it keeps the rest of the function free of nested ifs.
    if not target.is_dir():
        print(f"Error: '{target}' is not a valid directory.")
        return

    print(f"Organizing: {target}")


if __name__ == "__main__":
    main()