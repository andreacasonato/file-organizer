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

    files = sorted([
        item for item in target.iterdir()
        if item.is_file() and not item.is_symlink()
    ])

    if not files:
        print("No files found.")
        return

    for item in files:
        # NEW: Figure out where this file should go.
        #
        # item.suffix → the extension WITH the dot, e.g. ".py", ".PDF", ""
        # .lower()    → normalize case so ".JPG" and ".jpg" land in the same folder
        suffix = item.suffix.lower()

        # If there's no extension (suffix == ""), use a catch-all folder name.
        # Otherwise strip the leading dot: ".py" → "py", ".jpg" → "jpg"
        if suffix == "":
            folder_name = "no_extension"
        else:
            folder_name = suffix[1:]   # [1:] means "skip the first character"

        # NEW: Build the full destination path.
        # The / operator on Path objects joins paths — no string concatenation needed.
        # e.g.  target / "jpg"  →  /home/user/downloads/jpg
        dest_dir = target / folder_name

        print(f"  {item.name:30s} → {dest_dir.name}/")


if __name__ == "__main__":
    main()