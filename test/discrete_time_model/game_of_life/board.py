from random import random
from typing import List

from dynamic_system.models.dynamic_system import DynamicSystem
from test.discrete_time_model.game_of_life.cell import Cell


class Board:
    _ds: DynamicSystem
    _cells: List[List[Cell]]

    def __init__(self, width: int = 10, height: int = 10):
        self._ds = DynamicSystem()
        self._fillBoard(width, height)
        self._defineRelations()

    def _fillBoard(self, width: int, height: int):
        self._cells = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(self._ds, i, j, state=random() < 0.5))
            self._cells.append(row)

    def _defineRelations(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                for x in range(max(0, i - 1), min(i + 2, len(self._cells))):
                    for y in range(max(0, j - 1), min(j + 2, len(self._cells[i]))):
                        if x != i or y != j:
                            self._cells[i][j].add(self._cells[x][y])

    def nextGeneration(self):
        self._ds.getOutput()
        self._ds.stateTransition()

    def show(self):
        self._ds.getOutput()
        for row in self._cells:
            for cell in row:
                print(str(cell), end="")
            print()