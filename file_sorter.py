"""
file_sorter.py
---------------
Sorts files in a given folder by type (based on their extension),
moving them into subfolders: Images, Documents, Videos, Audio,
Archives, Code, Others.

How it works:
1. Look at each file's extension in the folder (.jpg, .pdf, .mp3, etc.)
2. Map that extension to a category (Images, Documents...).
3. Create a subfolder for that category (if it doesn't exist yet)
   and move the file into it.

Usage:
    python file_sorter.py "C:/Users/Me/Downloads"
    python file_sorter.py /home/user/downloads --dry-run
"""

import argparse
import shutil
import sys
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".csv", ".odt"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".java", ".cpp", ".c", ".sh", ".ipynb"},
}


def get_category(extension: str) -> str:
    """Returns the category name for a given file extension."""
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def unique_target_path(target_dir: Path, filename: str) -> Path:
    """If a file with this name already exists in the target folder, finds a free name."""
    target_path = target_dir / filename
    if not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    counter = 1
    while target_path.exists():
        target_path = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1
    return target_path


def sort_folder(folder_path: Path, dry_run: bool = False) -> dict:
    """Sorts files into category subfolders. Returns stats {category: file count}."""
    stats: dict[str, int] = {}

    for item in folder_path.iterdir():
        if item.is_dir():
            continue  # skip folders (including already-created category folders)

        category = get_category(item.suffix)
        stats[category] = stats.get(category, 0) + 1

        if dry_run:
            print(f"[dry-run] {item.name}  ->  {category}/")
            continue

        target_dir = folder_path / category
        target_dir.mkdir(exist_ok=True)
        target_path = unique_target_path(target_dir, item.name)

        try:
            shutil.move(str(item), str(target_path))
            print(f"{item.name}  ->  {category}/{target_path.name}")
        except OSError as e:
            print(f"Could not move {item.name}: {e}", file=sys.stderr)

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Sorts files in a folder by type (extension).")
    parser.add_argument("folder", help="Path to the folder to sort")
    parser.add_argument("--dry-run", action="store_true", help="Only show the plan, don't move any files")
    args = parser.parse_args()

    folder_path = Path(args.folder).expanduser().resolve()

    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Folder not found: {folder_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Sorting files in: {folder_path}\n")
    stats = sort_folder(folder_path, dry_run=args.dry_run)

    print("\nSummary:")
    if not stats:
        print("  No files to sort (or everything is already sorted).")
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} file(s)")


if __name__ == "__main__":
    main()
