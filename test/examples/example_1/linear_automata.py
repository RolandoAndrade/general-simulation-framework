from random import random, seed
from typing import List

from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from examples.example_1.cell import Cell


class LinearAutomata(DiscreteEventDynamicSystem):
    """Linear Automata implementation

    It has a group of cells, connected between them. The output cells of each cell are all its neighbors.
    Attributes:
        _cells (List[Cell]): Group of cells of the linear automata.
    """
    _cells: List[Cell]

    def __init__(self, cells: int = 5, random_seed: int = 42):
        """
        Args:
            cells (int): Number of cells of the automata.
            random_seed (int): Random seed for determinate the state of the seeds.
        """
        super().__init__()
        seed(random_seed)
        self._create_cells(cells)
        self._create_relations(cells)

    def _create_cells(self, cells: int):
        """Appends the cells to the automata.
        Args:
            cells (int): Number of cells of the automata.
        """
        self._cells = []
        for i in range(cells):
            is_alive = random() < 0.5
            self._cells.append(Cell(self, is_alive))

    def _create_relations(self, cells: int):
        """Creates the connections between the left cell and the right cell.
        Args:
            cells (int): Number of cells of the automata.
        """
        for i in range(cells):
            self._cells[i-1].add(self._cells[i])

    def __str__(self):
        """Changes the format to show the linear automata when is printed"""
        s = ""
        for cell in self._cells:
            s += str(cell)
        return s
