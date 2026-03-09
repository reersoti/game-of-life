# Custom Game of Life

Interactive implementation of Conway's Game of Life with support for:

- classic and custom birth/survival rules (`B3/S23` format)
- 4-neighbor and 8-neighbor modes
- custom 3x3 neighborhood template
- manual board editing with mouse input
- CSV export of simulation frames

## Project structure

```text
custom-game-of-life/
├── game_of_life/
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.py
│   ├── grid.py
│   ├── gui.py
│   ├── main.py
│   └── simulation.py
├── input.txt
├── requirements.txt
├── run.py
└── README.md
```

## Requirements

- Python 3.10+
- Tkinter
- NumPy

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

Or as a package:

```bash
python -m game_of_life
```

## Controls

- **Left click** — toggle a cell
- **Drag with left button** — draw live cells
- **Space** — execute one step
- **Start / Pause** — start or stop simulation
- **Clear / Reset** — clear the board

## Configuration

`input.txt` stores:

1. board size in pixels
2. cell size in pixels

Example:

```text
800
20
```

## Notes

- The board uses wrap-around behavior on edges.
- Simulation frames are exported to `log.csv` after closing the app.
