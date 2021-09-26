import unittest

from gsf.core.entity.core import static_entity_manager
from gsf.dynamic_system import BaseDynamicSystem
from gsf.dynamic_system.future_event_list import Scheduler
from gsf.models import BaseModel
from test.module_tests.mocks.base_model_mock import BaseModelMock
from test.module_tests.mocks.dynamic_system_mock import DynamicSystemMock


class BaseModelTest(unittest.TestCase):
    """Base model tests"""

    dynamic_system: BaseDynamicSystem
    model: BaseModel

    def setUp(self) -> None:
        """Sets up tests"""
        self.dynamic_system = DynamicSystemMock(Scheduler())
        self.model = BaseModelMock(self.dynamic_system, "model")

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        static_entity_manager._saved_names = set()

    def test_set_name(self):
        """Test the serialization of the name."""
        self.assertEqual(self.model.get_id(), "model")
        m = BaseModelMock(self.dynamic_system)
        n = BaseModelMock(self.dynamic_system)
        self.assertEqual("model0", m.get_id())
        self.assertEqual("model1", n.get_id())
        try:
            BaseModelMock(self.dynamic_system, "model1")
            self.assertTrue(False)
        except NameError:
            self.assertTrue(True)

    def test_set_state(self):
        """Test the state of the model"""
        self.model.set_up_state({"x": 1, "y": 0})
        saved_state = self.model.get_state()
        self.assertDictEqual({"x": 1, "y": 0}, saved_state)

    def test_add_another_model(self):
        """Test the state of the model"""
        m2 = BaseModelMock(self.dynamic_system, "model 2")
        self.model.add(m2)
        paths = self.dynamic_system._paths.get(self.model)
        for p in paths:
            self.assertEqual(self.model, p.get_source_model())
            self.assertEqual(m2, p.get_destination_model())

    def test_remove_model(self):
        """Test removal of the model"""
        self.model.remove()
        self.assertEqual(0, len(self.dynamic_system._models))

    def test_remove_model_with_path(self):
        """Test removal of the model with a path"""
        m2 = BaseModelMock(self.dynamic_system, "model 2")
        self.model.add(m2)
        self.assertEqual(2, len(self.dynamic_system._models))
        self.assertEqual(1, len(self.dynamic_system._paths))
        self.model.remove()
        self.assertEqual(1, len(self.dynamic_system._models))
        self.assertEqual(0, len(self.dynamic_system._paths))

    def test_get_dynamic_system(self):
        """Should return the dynamic system"""
        ds = self.model.get_dynamic_system()
        self.assertEqual(self.dynamic_system, ds)
