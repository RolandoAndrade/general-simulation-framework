import unittest

from models.core import Path
from test.mocks.model_mock import ModelMock


class PathTest(unittest.TestCase):
    def test_path_creation(self):
        """Should create a path"""
        model_mock = ModelMock()
        path = Path()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
