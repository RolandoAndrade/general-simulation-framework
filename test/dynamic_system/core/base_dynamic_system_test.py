import unittest

from core.entity.core import Entity
from core.entity.properties import ExpressionProperty
from core.mathematics.values.value import Value
from dynamic_system.core import BaseDynamicSystem
from dynamic_system.future_event_list import Scheduler
from models.core import Path
from test.mocks.base_model_mock import BaseModelMock
from test.mocks.dynamic_system_mock import DynamicSystemMock


class BaseDynamicSystemTest(unittest.TestCase):
    """Base dynamic system tests"""

    dynamic_system: BaseDynamicSystem

    def setUp(self) -> None:
        """Sets up tests"""
        self.dynamic_system = DynamicSystemMock(Scheduler())

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        Entity._saved_names = set()

    def test_add_model(self) -> None:
        """Adds models to the dynamic system."""
        models = set()
        for i in range(3):
            model = BaseModelMock(self.dynamic_system)
            models.add(model)
        self.assertEqual(models, self.dynamic_system._models)

    def test_link(self) -> None:
        """Adds paths to the dynamic system."""
        m1 = BaseModelMock(self.dynamic_system)
        m2 = BaseModelMock(self.dynamic_system)
        m3 = BaseModelMock(self.dynamic_system)
        m1.add(m2)
        m2.add(m3)
        m12 = self.dynamic_system._paths[m1].pop()
        m23 = self.dynamic_system._paths[m2].pop()
        self.assertEqual(m12.get_source_model(), m1)
        self.assertEqual(m12.get_destination_model(), m2)
        self.assertEqual(m23.get_source_model(), m2)
        self.assertEqual(m23.get_destination_model(), m3)

    def test_remove_model(self) -> None:
        """Removes a model of the dynamic system."""
        m1 = BaseModelMock(self.dynamic_system)
        m2 = BaseModelMock(self.dynamic_system)
        m3 = BaseModelMock(self.dynamic_system)
        self.dynamic_system.remove(m2)
        self.assertEqual({m1, m3}, self.dynamic_system._models)

    def test_remove_path(self) -> None:
        """Removes a model of the dynamic system."""
        m1 = BaseModelMock(self.dynamic_system)
        m2 = BaseModelMock(self.dynamic_system)
        m3 = BaseModelMock(self.dynamic_system)
        m12 = Path(m1, m2, ExpressionProperty(Value(1)))
        m23 = Path(m2, m3, ExpressionProperty(Value(1)))
        self.dynamic_system.link(m12)
        self.dynamic_system.link(m23)
        self.assertEqual({m12}, self.dynamic_system._paths[m1])
        self.dynamic_system.unlink(m12)
        self.assertTrue(m1 not in self.dynamic_system._paths)

    def test_remove_model_and_path(self) -> None:
        """Removes a model of the dynamic system."""
        m1 = BaseModelMock(self.dynamic_system)
        m2 = BaseModelMock(self.dynamic_system)
        m3 = BaseModelMock(self.dynamic_system)
        m12 = Path(m1, m2, ExpressionProperty(Value(1)))
        m23 = Path(m2, m3, ExpressionProperty(Value(1)))
        m13 = Path(m1, m3, ExpressionProperty(Value(1)))
        m31 = Path(m3, m1, ExpressionProperty(Value(1)))
        m32 = Path(m3, m2, ExpressionProperty(Value(1)))
        self.dynamic_system.link(m12)
        self.dynamic_system.link(m23)
        self.dynamic_system.link(m13)
        self.dynamic_system.link(m31)
        self.dynamic_system.link(m32)

        self.assertEqual({m12, m13}, self.dynamic_system._paths[m1])
        self.assertEqual({m31, m32}, self.dynamic_system._paths[m3])

        self.dynamic_system.remove(m1)

        self.assertTrue(m1 not in self.dynamic_system._paths)
        self.assertEqual({m32}, self.dynamic_system._paths[m3])

    def test_show(self) -> None:
        """Shows a diagram of the dynamic system"""
        m1 = BaseModelMock(self.dynamic_system)
        m2 = BaseModelMock(self.dynamic_system)
        m3 = BaseModelMock(self.dynamic_system)
        m1.add(m2)
        m2.add(m3)
        m3.add(m1)
        m1.add(m1)
        self.dynamic_system.show()


if __name__ == "__main__":
    unittest.main()
