from pathlib import Path
from typing import Tuple


def read_config(path: str | Path = "input.txt") -> Tuple[int, int]:
    """Read board size and cell size from a small text config file."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        board_size = int(file.readline().strip())
        cell_size = int(file.readline().strip())
    return board_size, cell_size
