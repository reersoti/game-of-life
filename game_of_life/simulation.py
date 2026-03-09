from __future__ import annotations

from .grid import Grid

DEFAULT_BIRTH = [3]
DEFAULT_SURVIVE = [2, 3]


class Simulation:
    def __init__(self, size: int, cell_size: int, offsets: list[tuple[int, int]]) -> None:
        self.grid = Grid(size=size, cell_size=cell_size, offsets=offsets)
        self._buffer = Grid(size=size, cell_size=cell_size, offsets=offsets)
        self.birth = DEFAULT_BIRTH.copy()
        self.survive = DEFAULT_SURVIVE.copy()

    def set_rules(self, rule_str: str) -> None:
        """Parse rules in B3/S23 format. Falls back to Conway defaults."""
        try:
            parts = rule_str.upper().split("/")
            self.birth = [int(x) for x in parts[0][1:]] if parts[0].startswith("B") else []
            self.survive = [int(x) for x in parts[1][1:]] if len(parts) > 1 and parts[1].startswith("S") else []
        except (ValueError, IndexError):
            self.birth = DEFAULT_BIRTH.copy()
            self.survive = DEFAULT_SURVIVE.copy()

    def count_live_neighbors(self, row: int, column: int) -> int:
        count = 0
        for d_row, d_col in self.grid.offsets:
            new_row = (row + d_row) % self.grid.cell_count
            new_col = (column + d_col) % self.grid.cell_count
            count += int(self.grid.cells[new_row, new_col] == 1)
        return count

    def update(self) -> None:
        for row in range(self.grid.cell_count):
            for column in range(self.grid.cell_count):
                live_neighbors = self.count_live_neighbors(row, column)
                current_value = self.grid.cells[row, column]

                if current_value == 1:
                    self._buffer.cells[row, column] = int(live_neighbors in self.survive)
                else:
                    self._buffer.cells[row, column] = int(live_neighbors in self.birth)

        self.grid.cells[:, :] = self._buffer.cells[:, :]
