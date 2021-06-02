from random import random, seed
from typing import List

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from simulation.simulation_engines.discrete_event_simulation_engine import (
    DiscreteEventSimulationEngine,
)
from test.model.game_of_life.cell import Cell
from reports.report_generators.default_report import DefaultReport

class Board:
    _sim: DiscreteEventSimulationEngine
    _cells: List[List[Cell]]
    _report: DefaultReport
    _generation: int

    def __init__(self, width: int = 10, height: int = 10, randomSeed: int = 42):
        seed(randomSeed)
        self._fillBoard(width, height)
        self._defineRelations()
        self._generation = 0

    def _fillBoard(self, width: int, height: int):
        ds = DiscreteEventDynamicSystem()
        self._report = DefaultReport()
        self._sim = DiscreteEventSimulationEngine(ds, self._report)
        self._cells = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(ds, i, j, state=random() < 0.5))
            self._cells.append(row)

    def _defineRelations(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                for x in range(max(0, i - 1), min(i + 2, len(self._cells))):
                    for y in range(max(0, j - 1), min(j + 2, len(self._cells[i]))):
                        if x != i or y != j:
                            self._cells[i][j].add(self._cells[x][y])

    def nextGeneration(self):
        self._generation = self._generation + 1
        self._sim.computeNextState(None, self._generation)

    def show(self):
        for row in self._cells:
            for cell in row:
                print(str(cell), end="")
            print()

    def simReport(self):
        print(self._report.generateReport())
