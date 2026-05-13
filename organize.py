#!/usr/bin/env python3
"""File organizer: sort files into subfolders by extension."""

import argparse
# NEW: shutil (shell utilities) is a standard library module for file operations.
# We use shutil.move() instead of Path.rename() because rename() breaks when
# source and destination are on different drives (e.g. SSD → USB stick).
# shutil.move() handles both cases transparently.
import shutil
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
        suffix = item.suffix.lower()
        folder_name = "no_extension" if suffix == "" else suffix[1:]
        dest_dir = target / folder_name
        dest_path = dest_dir / item.name   # full path including filename

        # NEW: Skip if a file with the same name already exists at the destination.
        # This is a safety guard — we never silently overwrite existing files.
        if dest_path.exists():
            print(f"  [SKIP]  '{item.name}' already exists in '{folder_name}/'")
            continue   # skip to the next file in the loop

        # NEW: Create the destination folder if it doesn't exist yet.
        # exist_ok=True means "don't raise an error if the folder already exists"
        # parents=False (default) means we only create ONE level, not a whole tree.
        dest_dir.mkdir(exist_ok=True)

        # NEW: Move the file.
        # str() is needed because shutil.move() expects strings, not Path objects
        # in older Python versions. Harmless on modern Python, good habit.
        shutil.move(str(item), dest_path)
        print(f"  [MOVED] '{item.name}' → '{folder_name}/'")

    print("\nDone.")


if __name__ == "__main__":
    main()