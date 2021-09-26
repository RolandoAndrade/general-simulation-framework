import unittest
from random import seed

from test.prototypes.prototype_2.board import Board


class Prototype1Test(unittest.TestCase):
    def setUp(self) -> None:
        seed(42)

    def test_validation(self):
        board = Board(10, 10)
        print(board)
        board.run_generations(10)
        print(board)


if __name__ == "__main__":
    unittest.main()
