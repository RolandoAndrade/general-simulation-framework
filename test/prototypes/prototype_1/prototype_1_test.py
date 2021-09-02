import unittest

from test.prototypes.prototype_1.cell import Cell


class Prototype1Test(unittest.TestCase):
    def test_validation(self):
        cell_1 = Cell(True)
        cell_2 = Cell(False)
        cell_3 = Cell(True)
        out = {}
        for i in range(3):
            out = {
                cell_1.get_id(): cell_1.get_output(),
                cell_2.get_id(): cell_2.get_output(),
                cell_3.get_id(): cell_3.get_output(),
            }
            cell_1.state_transition(inputs={cell_3.get_id(): out[cell_3.get_id()]})
            cell_2.state_transition(inputs={cell_1.get_id(): out[cell_1.get_id()]})
            cell_3.state_transition(inputs={cell_2.get_id(): out[cell_2.get_id()]})

        self.assertEqual([False, True, True], list(out.values()))


if __name__ == "__main__":
    unittest.main()
