import unittest

from test.discrete_time_model.game_of_life.board import Board


class TestGameOfLife(unittest.TestCase):
    def test_game(self):
        self.board = Board(20, 20)
        self.board.show()
        for i in range(10):
            print()
            self.board.nextGeneration()
            self.board.show()


if __name__ == '__main__':
    unittest.main()
