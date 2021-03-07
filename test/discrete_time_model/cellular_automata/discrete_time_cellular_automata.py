import unittest

from test.discrete_time_model.cellular_automata.cell import Cell


class CellularAutomata(unittest.TestCase):
    def setUp(self) -> None:
        self.cellA = Cell(Cell.ALIVE)
        self.cellB = Cell(Cell.DEAD)
        self.cellC = Cell(Cell.DEAD)

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


if __name__ == '__main__':
    unittest.main()
