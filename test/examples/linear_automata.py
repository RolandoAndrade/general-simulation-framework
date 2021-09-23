from random import random, seed
from typing import List

from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from examples.cell import Cell


class LinearAutomata(DiscreteEventDynamicSystem):
    _cells = List[Cell]

    def __init__(self, cells: int = 5, random_seed: int = 42):
        super().__init__()
        seed(random_seed)
        self._create_cells(cells)
        self._create_relations(cells)

    def _create_cells(self, cells: int):
        self._cells = []
        for i in range(cells):
            is_alive = random() < 0.5
            self._cells.append(Cell(self, is_alive))

    def _create_relations(self, cells: int):
        for i in range(cells):
            self._cells[i-1].add(self._cells[i])

    def __str__(self):
        s = ""
        for cell in self._cells:
            s += str(cell)
        return s
