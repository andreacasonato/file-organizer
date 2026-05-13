#!/usr/bin/env python3
"""File organizer: sort files into subfolders by extension."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Organize files by extension."
    )
    parser.add_argument("directory", help="Path to the directory you want to organize")
    args = parser.parse_args()

    target = Path(args.directory).resolve()
    if not target.is_dir():
        print(f"Error: '{target}' is not a valid directory.")
        return

    print(f"Organizing: {target}\n")

    # NEW: Collect every item in the directory, but keep only plain files.
    #
    # target.iterdir() yields every item (files, folders, symlinks) one by one.
    # We build a list with a "list comprehension" — a compact Python loop:
    #
    #   [item for item in <iterable> if <condition>]
    #
    # The two conditions:
    #   item.is_file()    → True for regular files only (excludes folders)
    #   not item.is_symlink() → excludes symbolic links (shortcuts);
    #                           moving a symlink instead of its target causes bugs
    #
    # sorted() makes the output predictable — alphabetical order every time.
    files = sorted([
        item for item in target.iterdir()
        if item.is_file() and not item.is_symlink()
    ])

    if not files:
        print("No files found.")
        return

    for item in files:
        print(item.name)


if __name__ == "__main__":
    main()