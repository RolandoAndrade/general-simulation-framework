import unittest

from test.model.game_of_life.board import Board

class TestGameOfLife(unittest.TestCase):
    def test_game(self):
        self.board = Board(10, 10, 42)
        self.board.show()
        for i in range(10):
            print("generation " + str(i + 1))
            self.board.nextGeneration()
            self.board.show()


if __name__ == '__main__':
    unittest.main()
