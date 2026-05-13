#!/usr/bin/env python3
"""File organizer: sort files into subfolders by extension."""

import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Organize files by extension."
    )
    parser.add_argument("directory", help="Path to the directory you want to organize")

    # NEW: add --dry-run as an optional flag.
    # action="store_true" means: if the user types --dry-run, args.dry_run = True
    #                            if they omit it,              args.dry_run = False
    # Note: argparse converts the dash to an underscore → dry_run (not dry-run).
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without moving any files"
    )

    args = parser.parse_args()
    dry_run: bool = args.dry_run   # store in a plain variable for clarity

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

        # NEW: Branch on dry_run BEFORE touching the filesystem.
        # In dry-run mode we only print — mkdir() and shutil.move() are never called.
        # This makes testing safe: you can point the script at real folders
        # and see exactly what it would do without risking any data.
        if dry_run:
            print(f"  [DRY-RUN]  Would move '{item.name}' → '{folder_name}/'")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), dest_path)
            print(f"  [MOVED]    '{item.name}' → '{folder_name}/'")

    print("\nDone.")


if __name__ == "__main__":
    main()