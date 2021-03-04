import unittest

from test.cellular_automata.dynamic_system.cell import Cell


class TestAutomata(unittest.TestCase):
    def setUp(self) -> None:
        self.c1 = Cell(Cell.ALIVE)
        self.c2 = Cell(Cell.DEAD)
        self.c3 = Cell(Cell.DEAD)
        self.c4 = Cell(Cell.DEAD)
        self.c1.add(self.c4)
        self.c2.add(self.c1)
        self.c3.add(self.c2)
        self.c4.add(self.c3)

    def test_something(self):
        self.c1.computeOutput()
        print(self.c2._input_manager._inputs)
        print(self.c1._last_inputs)


if __name__ == '__main__':
    unittest.main()
