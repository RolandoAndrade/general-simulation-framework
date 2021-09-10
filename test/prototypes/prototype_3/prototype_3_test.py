import unittest

from test.prototypes.prototype_3.assembly_line import AssemblyLine


class Prototype3Test(unittest.TestCase):
    def test_something(self):
        assembly_line = AssemblyLine()
        i = assembly_line.process([1, 2, None, None, None, None, None, None])
        self.assertEqual(7, i)


if __name__ == "__main__":
    unittest.main()
