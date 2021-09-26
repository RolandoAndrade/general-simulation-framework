from random import random
from typing import List

from gsf.core.types import Time
from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from test.prototypes.prototype_2.cell import Cell


class Board(DiscreteEventDynamicSystem):
    _cells: List[List[Cell]]

    def __init__(self, width: int, height: int):
        super().__init__()
        self._fill_board(width, height)
        self._define_relations()

    def _fill_board(self, width: int, height: int):
        self._cells = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(random() < 0.5, self, i, j))
            self._cells.append(row)

    def _define_relations(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                for x in range(max(0, i - 1), min(i + 2, len(self._cells))):
                    for y in range(max(0, j - 1), min(j + 2, len(self._cells[i]))):
                        if x != i or y != j:
                            self._cells[i][j].add(self._cells[x][y])

    def run_generations(self, generations: int = 10):
        for i in range(generations):
            self.get_output()
            self.state_transition(event_time=Time(1))

    def __str__(self):
        s = ""
        for row in self._cells:
            for cell in row:
                s += str(cell)
            s += "\n"
        return s
