from __future__ import annotations

from pathlib import Path

from .config import read_config
from .gui import EIGHT_NEIGHBORS, GameOfLifeGUI


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    size, tile_size = read_config(project_root / "input.txt")
    app = GameOfLifeGUI(size=size, cell_size=tile_size, neighbor_offsets=EIGHT_NEIGHBORS)
    app.run()
    app.save_log_csv(project_root / "log.csv")


if __name__ == "__main__":
    main()
