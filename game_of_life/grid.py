from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np

Offset = tuple[int, int]


@dataclass
class Grid:
    size: int
    cell_size: int
    offsets: Sequence[Offset]
    cells: np.ndarray = field(init=False)
    cell_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.cell_count = self.size // self.cell_size
        self.cells = np.zeros((self.cell_count, self.cell_count), dtype=int)

    def clear(self) -> None:
        self.cells.fill(0)

    def set_offsets(self, offsets: Iterable[Offset]) -> None:
        self.offsets = list(offsets)
