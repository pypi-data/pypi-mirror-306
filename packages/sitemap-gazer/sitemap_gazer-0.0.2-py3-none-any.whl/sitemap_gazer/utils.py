from pathlib import Path
from datetime import datetime


def get_timestamped_dirs(data_dir: Path, limit: int = None) -> list[Path]:
    data_dirs = [
        d
        for d in data_dir.iterdir()
        if d.is_dir() and d.name.replace("_", "").isdigit()
    ]

    sorted_dirs = sorted(
        data_dirs,
        key=lambda d: datetime.strptime(d.name, "%Y%m%d_%H%M%S"),
        reverse=True,
    )

    return sorted_dirs[:limit] if limit else sorted_dirs
