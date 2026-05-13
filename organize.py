#!/usr/bin/env python3
"""
File organizer: scan a directory and sort files into subfolders by extension.

Usage:
    python organize.py <directory> [--dry-run] [--clean]

Flags:
    --dry-run   Preview moves without touching the filesystem
    --clean     Remove empty subfolders after organizing
"""

import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Organize files by extension."
    )
    parser.add_argument("directory", help="Path to the directory you want to organize")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without moving any files"
    )
    # NEW: --clean flag to remove empty subfolders after organizing.
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete empty subfolders after organizing"
    )

    args = parser.parse_args()
    dry_run: bool = args.dry_run

    target = Path(args.directory).resolve()
    if not target.is_dir():
        print(f"Error: '{target}' is not a valid directory.")
        return

    if dry_run:
        print("=== DRY-RUN: no files will be moved ===\n")

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
        dest_path = dest_dir / item.name

        if dest_path.exists():
            print(f"  [SKIP]     '{item.name}' already exists in '{folder_name}/'")
            continue

        if dry_run:
            print(f"  [DRY-RUN]  Would move '{item.name}' → '{folder_name}/'")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), dest_path)
            print(f"  [MOVED]    '{item.name}' → '{folder_name}/'")

    # NEW: If the user passed --clean, scan for empty subfolders and remove them.
    #
    # When does this happen? Example:
    #   Before running: downloads/jpg/photo.jpg   (jpg/ already existed)
    #   We move all .jpg files there — jpg/ is not empty, so we leave it alone.
    #   But if jpg/ was already empty before we started, --clean removes it.
    #
    # How it works:
    #   any(folder.iterdir()) --> True if the folder contains at least one item
    #   not any(...)          --> True only if the folder is completely empty
    #   folder.rmdir()        --> deletes the folder (only works on empty folders,
    #                           so this is safe — Python raises an error if not empty)
    if args.clean:
        print("\nCleaning empty folders…")
        for folder in sorted(target.iterdir()):
            if not folder.is_dir():
                continue
            if not any(folder.iterdir()):   # is the folder empty?
                if dry_run:
                    print(f"  [DRY-RUN]  Would remove empty folder: '{folder.name}/'")
                else:
                    folder.rmdir()
                    print(f"  [REMOVED]  Empty folder: '{folder.name}/'")

    print("\nDone.")


if __name__ == "__main__":
    main()