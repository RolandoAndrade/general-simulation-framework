import unittest

from gsf.core.entity.core import static_entity_manager
from gsf.core.entity.properties import ExpressionProperty
from gsf.core.mathematics.values import Value
from gsf.dynamic_system import BaseDynamicSystem
from gsf.models import Path, BaseModel
from test.module_tests.mocks.base_model_mock import BaseModelMock
from test.module_tests.mocks.dynamic_system_mock import DynamicSystemMock


class PathTest(unittest.TestCase):
    """Path tests"""

    dynamic_system: BaseDynamicSystem

    model_1: BaseModel
    model_2: BaseModel
    path: Path

    def setUp(self) -> None:
        """Set ups tests"""
        self.dynamic_system = DynamicSystemMock()
        self.model_1 = BaseModelMock(self.dynamic_system, "model 1")
        self.model_2 = BaseModelMock(self.dynamic_system, "model 2")
        self.path = Path(self.model_1, self.model_2, ExpressionProperty(Value(1)))

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        static_entity_manager._saved_names = set()

    def test_get_source_model(self):
        """Should return the source model"""
        self.assertEqual(self.path.get_source_model(), self.model_1)

    def test_get_destination_model(self):
        """Should return the source model"""
        self.assertEqual(self.path.get_destination_model(), self.model_2)

    def test_get_weight(self):
        """Should return the weight of the path"""
        self.assertEqual(self.path.get_weight(), 1)

    def test_set_weight(self):
        """Should set the weight of the path"""
        self.path.set_weight(ExpressionProperty(Value(5)))
        self.assertEqual(self.path.get_weight(), 5)

    def test_get_properties(self):
        """Should return the properties of the path."""
        self.assertEqual(1, self.path.get_properties()["Weight"].get_value().evaluate())

    def test_get_equality(self):
        """Should check equality by path and by models"""
        self.assertTrue(self.path == self.path)
        self.assertTrue(self.path == self.model_1)
        self.assertTrue(self.path == self.model_2)
        self.assertFalse(self.path != self.path)
        self.assertFalse(self.path != self.model_1)
        self.assertFalse(self.path != self.model_2)


if __name__ == "__main__":
    unittest.main()
