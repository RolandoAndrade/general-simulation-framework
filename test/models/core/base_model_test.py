import unittest

from core.entity.core import Entity
from dynamic_system.core import BaseDynamicSystem
from models.core import BaseModel
from test.mocks.base_model_mock import BaseModelMock
from test.mocks.dynamic_system_mock import DynamicSystemMock


class BaseModelTest(unittest.TestCase):
    """Base model tests"""
    dynamic_system: BaseDynamicSystem
    model: BaseModel

    def setUp(self) -> None:
        """Sets up tests"""
        self.dynamic_system = DynamicSystemMock()
        self.model = BaseModelMock(self.dynamic_system, "model")

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        Entity._saved_names = set()

    def test_set_name(self):
        """Test the serialization of the name."""
        self.assertEqual(self.model.get_id(), "model")
        m = BaseModelMock(self.dynamic_system)
        n = BaseModelMock(self.dynamic_system)
        self.assertEqual("model0", m.get_id())
        self.assertEqual("model1", n.get_id())
        try:
            n = BaseModelMock(self.dynamic_system, "model1")
            self.assertTrue(False)
        except NameError:
            self.assertTrue(True)

    def test_set_state(self):
        """Test the state of the model"""
        self.model.set_up_state({
            "x": 1,
            "y": 0
        })
        saved_state = self.model.get_state()
        self.assertDictEqual({
            "x": 1,
            "y": 0
        }, saved_state)

    def test_add_another_model(self):
        """Test the state of the model"""
        self.model.set_up_state({
            "x": 1,
            "y": 0
        })
        saved_state = self.model.get_state()
        self.assertDictEqual({
            "x": 1,
            "y": 0
        }, saved_state)

