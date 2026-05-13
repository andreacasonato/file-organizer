#!/usr/bin/env python3
"""File organizer: sort files into subfolders by extension."""

# argparse lets users pass arguments on the command line:
#   python organize.py /some/folder
# Without it the script would always work on a hardcoded path — not useful.
import argparse


def main():
    # 1. Create the parser and describe what this script does
    parser = argparse.ArgumentParser(
        description="Organize files by extension."
    )

    # 2. Register the one argument we need: the directory to organize
    #    "directory" (no dashes) = positional argument → always required
    parser.add_argument(
        "directory",
        help="Path to the directory you want to organize"
    )

    # 3. Parse whatever the user typed and store results in `args`
    #    After this line:  args.directory == "/some/folder"
    args = parser.parse_args()

    # Temporary: just prove we received the argument correctly
    print(f"Target directory: {args.directory}")


# This guard means main() only runs when you execute THIS file directly.
# If another script imports organize.py, main() stays silent.
if __name__ == "__main__":
    main()