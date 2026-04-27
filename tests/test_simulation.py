import tempfile
import unittest
from pathlib import Path

from game_of_life.config import read_config
from game_of_life.gui import EIGHT_NEIGHBORS
from game_of_life.simulation import DEFAULT_BIRTH, DEFAULT_SURVIVE, Simulation


class ConfigTests(unittest.TestCase):
    def test_read_config_returns_board_and_cell_size(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "input.txt"
            config_path.write_text("100\n10\n", encoding="utf-8")

            board_size, cell_size = read_config(config_path)

        self.assertEqual(board_size, 100)
        self.assertEqual(cell_size, 10)


class SimulationTests(unittest.TestCase):
    def test_default_rules_are_conway_rules(self) -> None:
        simulation = Simulation(size=30, cell_size=10, offsets=EIGHT_NEIGHBORS)

        self.assertEqual(simulation.birth, DEFAULT_BIRTH)
        self.assertEqual(simulation.survive, DEFAULT_SURVIVE)

    def test_invalid_rule_falls_back_to_default_rules(self) -> None:
        simulation = Simulation(size=30, cell_size=10, offsets=EIGHT_NEIGHBORS)

        simulation.set_rules("invalid")

        self.assertEqual(simulation.birth, DEFAULT_BIRTH)
        self.assertEqual(simulation.survive, DEFAULT_SURVIVE)

    def test_block_pattern_stays_stable(self) -> None:
        simulation = Simulation(size=40, cell_size=10, offsets=EIGHT_NEIGHBORS)
        simulation.grid.cells[1, 1] = 1
        simulation.grid.cells[1, 2] = 1
        simulation.grid.cells[2, 1] = 1
        simulation.grid.cells[2, 2] = 1

        before = simulation.grid.cells.copy()
        simulation.update()

        self.assertTrue((simulation.grid.cells == before).all())

    def test_blinker_pattern_oscillates(self) -> None:
        simulation = Simulation(size=50, cell_size=10, offsets=EIGHT_NEIGHBORS)
        simulation.grid.cells[2, 1] = 1
        simulation.grid.cells[2, 2] = 1
        simulation.grid.cells[2, 3] = 1

        simulation.update()

        self.assertEqual(simulation.grid.cells[1, 2], 1)
        self.assertEqual(simulation.grid.cells[2, 2], 1)
        self.assertEqual(simulation.grid.cells[3, 2], 1)
        self.assertEqual(int(simulation.grid.cells.sum()), 3)


if __name__ == "__main__":
    unittest.main()
