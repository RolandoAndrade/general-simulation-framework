import unittest

from dynamic_system.models.dynamic_system import DynamicSystem
from test.discrete_time_model.cellular_automata.cell import Cell


class CellularAutomata(unittest.TestCase):
    def setUp(self) -> None:
        self.ds = DynamicSystem()
        self.cellA = Cell(self.ds, Cell.ALIVE)
        self.cellB = Cell(self.ds)
        self.cellC = Cell(self.ds)
        self.cellA.add(self.cellC)
        self.cellB.add(self.cellA)
        self.cellC.add(self.cellB)

    def test_aca(self):
        ao = self.cellA.getOutput()
        bo = self.cellB.getOutput()
        co = self.cellC.getOutput()
        self.cellA.stateTransition(co)
        self.cellB.stateTransition(ao)
        self.cellC.stateTransition(bo)
        self.assertEqual(self.cellA.getOutput(), Cell.DEAD)
        self.assertEqual(self.cellB.getOutput(), Cell.ALIVE)
        self.assertEqual(self.cellC.getOutput(), Cell.DEAD)

    def test_dynamic_system(self):
        o = self.ds.getOutput()
        self.ds.stateTransition(o)
        self.assertEqual(self.cellA.getOutput(), Cell.DEAD)
        self.assertEqual(self.cellB.getOutput(), Cell.ALIVE)
        self.assertEqual(self.cellC.getOutput(), Cell.DEAD)



if __name__ == '__main__':
    unittest.main()
