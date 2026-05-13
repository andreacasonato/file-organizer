#!/usr/bin/env python3
"""File organizer: sort files into subfolders by extension."""

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Organize files by extension")
    parser.add_argument("directory", help="Directory to organize")
    args = parser.parse_args()

    target = Path(args.directory)
    if not target.is_dir():
        print(f"Error: {target} is not a directory.")
        return

    # List all items in the directory
    for item in target.iterdir():
        print(item.name)

if __name__ == "__main__":
    main()