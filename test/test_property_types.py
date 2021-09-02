import unittest

from core.entity import BooleanProperty
from core.entity import NumberProperty
from core.entity.properties.string_property import StringProperty


class MyTestCase(unittest.TestCase):
    def test_number(self):
        a = NumberProperty(5)
        self.assertEqual(2 + a, 7, "Error")
        a += 5
        self.assertEqual(a, 10, "Error")

    def test_bool(self):
        a = BooleanProperty(True)
        self.assertEqual(a == True, True, "a is true!")
        self.assertEqual(a == False, False, "a is not false!")

        a = BooleanProperty(False)
        self.assertEqual(a, False, "a is false!")
        self.assertEqual(not a, True, "a is not true!")

    def test_string(self):
        a = StringProperty("Hello")
        self.assertEqual(a + " World", "Hello World", "Error")


if __name__ == "__main__":
    unittest.main()
