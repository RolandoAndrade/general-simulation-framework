from __future__ import annotations
from random import random, seed
from typing import List

from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from examples.example_2.cell import Cell

class Board(DiscreteEventDynamicSystem):
    """Game of life

    It has a group of cells, connected between them. The output of each cell is its right neighbor.
    Attributes:
        _cells (List[List[Cell]]): Group of cells of the board automata.
    """
    _cells: List[List[Cell]]

    def __init__(self, width: int, height: int, random_seed: int = 42):
        super().__init__()
        seed(random_seed)
        self._create_cells(width, height)
        self._define_relations(width, height)

    def _create_cells(self, width: int, height: int):
        """Appends the cells to the automata.
        Args:
            width (int): Number of column cells of the automata.
            height (int): Number of row cells of the automata.
        """
        self._cells = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(self, random() < 0.5))
            self._cells.append(row)

    def _define_relations(self, width: int, height: int):
        """Creates the connections between the left cell and the right cell.
        Args:
            width (int): Number of column cells of the automata.
            height (int): Number of row cells of the automata.
        """
        for i in range(height):
            for j in range(width):
                for x in range(max(0, i - 1), min(i + 2, height)):
                    for y in range(max(0, j - 1), min(j + 2, width)):
                        if x != i or y != j:
                            self._cells[i][j].add(self._cells[x][y])

    def __str__(self):
        """Changes the format to show the board automata when is printed"""
        s = ""
        for row in self._cells:
            for cell in row:
                s += str(cell)
            s += "\n"
        return s

    def get_output(self) -> DynamicSystemOutput:
        print(self)
        return super().get_output()
