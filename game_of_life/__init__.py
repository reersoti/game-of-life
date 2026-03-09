"""Customizable Conway's Game of Life package."""

from .config import read_config
from .gui import GameOfLifeGUI
from .simulation import Simulation

__all__ = ["GameOfLifeGUI", "Simulation", "read_config"]
