# File Organizer

Sorts files in a directory into subfolders by extension.

## Usage

```bash
python organize.py <directory> [--dry-run] [--clean]
```

| Flag | What it does |
|---|---|
| *(none)* | Move files into subfolders |
| `--dry-run` | Preview what would happen, nothing is moved |
| `--clean` | Remove empty folders after organizing |

## Example

```
downloads/
  photo.jpg   → downloads/jpg/photo.jpg
  notes.txt   → downloads/txt/notes.txt
  script.py   → downloads/py/script.py
```
