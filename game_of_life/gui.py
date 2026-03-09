from __future__ import annotations

import tkinter as tk
from pathlib import Path

import numpy as np

from .simulation import Simulation

FOUR_NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
EIGHT_NEIGHBORS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


class GameOfLifeGUI:
    def __init__(self, size: int, cell_size: int, neighbor_offsets: list[tuple[int, int]]) -> None:
        self.simulation = Simulation(size, cell_size, neighbor_offsets)
        self.is_running = False
        self.update_interval_ms = 200
        self.log: list[np.ndarray] = []

        self.root = tk.Tk()
        self.root.title("Game of Life — custom neighborhood")

        self._build_layout(size)
        self._draw_grid_lines()
        self._create_cell_rectangles()
        self._bind_events()
        self._apply_neighbor_grid_to_offsets()

    def _build_layout(self, size: int) -> None:
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(left_frame, width=size, height=size, bg="white")
        self.canvas.pack()

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="y", padx=8, pady=8)

        controls_frame = tk.Frame(right_frame)
        controls_frame.pack(side="top", pady=5)

        tk.Label(controls_frame, text="Cycles:").pack(side="left", padx=4)
        self.cycle_entry = tk.Entry(controls_frame, width=6)
        self.cycle_entry.insert(0, "0")
        self.cycle_entry.pack(side="left", padx=4)

        self.start_button = tk.Button(controls_frame, text="Start", command=self._toggle_run)
        self.start_button.pack(side="left", padx=4)
        tk.Button(controls_frame, text="Clear", command=self._clear).pack(side="left", padx=4)
        tk.Button(controls_frame, text="Reset", command=self._reset).pack(side="left", padx=4)

        self.neighbor_type = tk.StringVar(value="8 neighbors")
        tk.OptionMenu(controls_frame, self.neighbor_type, "8 neighbors", "4 neighbors").pack(side="left", padx=5)

        rules_frame = tk.Frame(right_frame)
        rules_frame.pack(side="top", pady=6)
        tk.Label(rules_frame, text="Rules (B/S):").pack(side="left", padx=4)
        self.rule_entry = tk.Entry(rules_frame, width=8)
        self.rule_entry.insert(0, "B3/S23")
        self.rule_entry.pack(side="left", padx=4)

        self.use_custom_rules = tk.BooleanVar(value=True)
        tk.Checkbutton(
            rules_frame,
            text="Use custom rule and neighborhood",
            variable=self.use_custom_rules,
        ).pack(side="left", padx=4)

        self.neighbor_grid = np.zeros((3, 3), dtype=int)
        self.neighbor_grid[1, 1] = 1
        pixel = self.simulation.grid.cell_size
        self.neighbor_canvas = tk.Canvas(right_frame, width=3 * pixel, height=3 * pixel, bg="white")
        self.neighbor_canvas.pack(pady=10)
        self.neighbor_cells = np.zeros((3, 3), dtype=object)

        for row in range(3):
            for col in range(3):
                x1, y1 = col * pixel, row * pixel
                x2, y2 = x1 + pixel, y1 + pixel
                color = "red" if (row, col) == (1, 1) else "white"
                rect_id = self.neighbor_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                self.neighbor_cells[row, col] = rect_id

    def _bind_events(self) -> None:
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.neighbor_canvas.bind("<Button-1>", self._on_neighbor_click)
        self.root.bind("<space>", lambda _event: self.step_once())

    def _draw_grid_lines(self) -> None:
        n = self.simulation.grid.cell_count
        step = self.simulation.grid.cell_size
        for index in range(n + 1):
            coord = index * step
            self.canvas.create_line(0, coord, self.simulation.grid.size, coord, fill="black")
            self.canvas.create_line(coord, 0, coord, self.simulation.grid.size, fill="black")

    def _create_cell_rectangles(self) -> None:
        n = self.simulation.grid.cell_count
        self.rect_ids = np.zeros((n, n), dtype=int)
        for row in range(n):
            for col in range(n):
                x1 = col * self.simulation.grid.cell_size
                y1 = row * self.simulation.grid.cell_size
                x2 = x1 + self.simulation.grid.cell_size
                y2 = y1 + self.simulation.grid.cell_size
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.rect_ids[row, col] = int(rect_id)

    def _draw_cell(self, row: int, col: int) -> None:
        color = "black" if self.simulation.grid.cells[row, col] == 1 else "white"
        self.canvas.itemconfig(int(self.rect_ids[row, col]), fill=color)

    def _draw_grid(self) -> None:
        for row in range(self.simulation.grid.cell_count):
            for col in range(self.simulation.grid.cell_count):
                self._draw_cell(row, col)

    def _on_click(self, event: tk.Event) -> None:
        col = event.x // self.simulation.grid.cell_size
        row = event.y // self.simulation.grid.cell_size
        if 0 <= row < self.simulation.grid.cell_count and 0 <= col < self.simulation.grid.cell_count:
            self.simulation.grid.cells[row, col] ^= 1
            self._draw_cell(row, col)

    def _on_drag(self, event: tk.Event) -> None:
        col = event.x // self.simulation.grid.cell_size
        row = event.y // self.simulation.grid.cell_size
        if 0 <= row < self.simulation.grid.cell_count and 0 <= col < self.simulation.grid.cell_count:
            if self.simulation.grid.cells[row, col] == 0:
                self.simulation.grid.cells[row, col] = 1
                self._draw_cell(row, col)

    def _on_neighbor_click(self, event: tk.Event) -> None:
        pixel = self.simulation.grid.cell_size
        col = event.x // pixel
        row = event.y // pixel
        if not (0 <= row < 3 and 0 <= col < 3):
            return
        if (row, col) == (1, 1):
            return

        self.neighbor_grid[row, col] ^= 1
        color = "black" if self.neighbor_grid[row, col] else "white"
        self.neighbor_canvas.itemconfig(int(self.neighbor_cells[row, col]), fill=color)
        self._apply_neighbor_grid_to_offsets()

    def _apply_neighbor_grid_to_offsets(self) -> None:
        offsets: list[tuple[int, int]] = []
        for row in range(3):
            for col in range(3):
                if (row, col) == (1, 1):
                    continue
                if self.neighbor_grid[row, col] == 1:
                    offsets.append((row - 1, col - 1))
        self.simulation.grid.set_offsets(offsets)
        self.simulation._buffer.set_offsets(offsets)

    def _apply_selected_neighbor_mode(self) -> None:
        if self.use_custom_rules.get():
            self._apply_neighbor_grid_to_offsets()
            return

        offsets = FOUR_NEIGHBORS if self.neighbor_type.get() == "4 neighbors" else EIGHT_NEIGHBORS
        self.simulation.grid.set_offsets(offsets)
        self.simulation._buffer.set_offsets(offsets)

    def _apply_selected_rules(self) -> None:
        rule = self.rule_entry.get() if self.use_custom_rules.get() else "B3/S23"
        self.simulation.set_rules(rule)

    def _toggle_run(self) -> None:
        self.is_running = not self.is_running
        self.start_button.config(text="Pause" if self.is_running else "Start")
        if self.is_running:
            self._update_loop()

    def _update_loop(self) -> None:
        if not self.is_running:
            return

        self._apply_selected_neighbor_mode()
        self._apply_selected_rules()

        previous_state = self.simulation.grid.cells.copy()
        self.simulation.update()
        self.log.append(self.simulation.grid.cells.copy())

        changed_positions = np.where(previous_state != self.simulation.grid.cells)
        for row, col in zip(changed_positions[0], changed_positions[1]):
            self._draw_cell(row, col)

        self.root.after(self.update_interval_ms, self._update_loop)

    def step_once(self) -> None:
        self._apply_selected_neighbor_mode()
        self._apply_selected_rules()

        previous_state = self.simulation.grid.cells.copy()
        self.simulation.update()
        self.log.append(self.simulation.grid.cells.copy())

        changed_positions = np.where(previous_state != self.simulation.grid.cells)
        for row, col in zip(changed_positions[0], changed_positions[1]):
            self._draw_cell(row, col)

    def _clear(self) -> None:
        self.simulation.grid.clear()
        self._draw_grid()

    def _reset(self) -> None:
        self.simulation.grid.clear()
        self.log.clear()
        self._draw_grid()

    def save_log_csv(self, filename: str | Path = "log.csv") -> None:
        output_path = Path(filename)
        with output_path.open("w", encoding="utf-8") as file:
            for frame in self.log:
                np.savetxt(file, frame, fmt="%d", delimiter=",")
                file.write("\n")

    def run(self) -> None:
        self.root.mainloop()
