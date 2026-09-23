from collections.abc import Sequence
from pathlib import Path


def check_file_exists(file_path: str | Path) -> bool:
    """Check whether a file exists on the local filesystem."""
    return Path(file_path).is_file()


def remove_file_if_exists(file_path: str | Path) -> None:
    """Remove file from filesystem if it currently exists."""
    Path(file_path).unlink(missing_ok=True)


def rename_file(
    file_path: str | Path, prefix: str | None = None, ext: str | None = None
) -> str:
    """Return new filename string with optional prefix prepended and extension modified."""
    p = Path(file_path)
    base = f"{prefix}{p.name}" if prefix else p.name
    if ext:
        base = f"{Path(base).stem}{ext}"
    return base


def filter_by_extensions(item_list: Sequence[str], endings: Sequence[str]) -> list[str]:
    """Filter list of filenames, excluding items matching specified file extensions."""
    if not item_list:
        return []

    if not endings:
        return list(item_list)

    return [
        item for item in item_list if not any(item.lower().endswith(e) for e in endings)
    ]
