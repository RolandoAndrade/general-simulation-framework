import unittest
from decimal import Decimal

from core.entity.core import Entity
from core.entity.properties import ExpressionProperty
from core.mathematics.values.value import Value
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler
from models.core import Path
from test.module_tests.mocks.dynamic_system_mock import DynamicSystemMock
from test.module_tests.mocks.model_mock import ModelMock

import numpy as np


class DiscreteEventDynamicSystemTest(unittest.TestCase):
    """Base dynamic system tests"""

    dynamic_system: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        """Sets up tests"""
        self.dynamic_system = DynamicSystemMock(Scheduler())

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        Entity._saved_names = set()

    def test_schedule(self):
        """Should schedule a model"""
        m = ModelMock(self.dynamic_system)
        self.dynamic_system.schedule(m, Decimal(10))
        self.assertEqual(10, self.dynamic_system.get_time_of_next_events())

    def test_get_next_models(self):
        """Should retrieve the next models"""
        m1 = ModelMock(self.dynamic_system)
        m2 = ModelMock(self.dynamic_system)
        m3 = ModelMock(self.dynamic_system)
        self.dynamic_system.schedule(m1, Decimal(10))
        self.dynamic_system.schedule(m2, Decimal(10))
        self.dynamic_system.schedule(m3, Decimal(11))
        self.assertEqual({m1, m2}, self.dynamic_system.get_next_models())

    def test_get_output(self):
        """Should retrieve the next models"""
        m1 = ModelMock(self.dynamic_system)
        self.dynamic_system.schedule(m1, Decimal(10))
        m1.get_output = lambda: 5
        self.assertDictEqual({m1: 5}, self.dynamic_system.get_output())

    def test_get_effective_paths_ones(self):
        """Should get the valid paths for each output"""
        m1 = ModelMock(self.dynamic_system)
        m2 = ModelMock(self.dynamic_system)
        m3 = ModelMock(self.dynamic_system)

        m12 = Path(m1, m2, ExpressionProperty(Value(1)))
        m13 = Path(m1, m3, ExpressionProperty(Value(1)))
        m23 = Path(m2, m3, ExpressionProperty(Value(1)))

        self.dynamic_system.link(m12)
        self.dynamic_system.link(m13)
        self.dynamic_system.link(m23)

        m1.get_output = lambda: 5
        m2.get_output = lambda: 15
        m3.get_output = lambda: 25

        self.dynamic_system.schedule(m1, Decimal(10))
        self.dynamic_system.schedule(m2, Decimal(10))
        self.dynamic_system.schedule(m3, Decimal(10))

        self.dynamic_system.get_output()

        self.assertEqual({m12, m13}, self.dynamic_system._get_effective_paths(m1))
        self.assertEqual({m23}, self.dynamic_system._get_effective_paths(m2))

    def test_get_effective_paths_probability(self):
        """Should get the valid paths for each output probability"""
        m1 = ModelMock(self.dynamic_system)
        m2 = ModelMock(self.dynamic_system)
        m3 = ModelMock(self.dynamic_system)

        m11 = Path(m1, m1, ExpressionProperty(Value(0.1)))
        m12 = Path(m1, m2, ExpressionProperty(Value(0.3)))
        m13 = Path(m1, m3, ExpressionProperty(Value(0.6)))
        m23 = Path(m2, m3, ExpressionProperty(Value(1)))

        self.dynamic_system.link(m11)
        self.dynamic_system.link(m12)
        self.dynamic_system.link(m13)
        self.dynamic_system.link(m23)

        m1.get_output = lambda: 5
        m2.get_output = lambda: 15
        m3.get_output = lambda: 25

        self.dynamic_system.schedule(m1, Decimal(10))
        self.dynamic_system.schedule(m2, Decimal(10))
        self.dynamic_system.schedule(m3, Decimal(10))

        self.dynamic_system.get_output()

        self.assertEqual(1, len(self.dynamic_system._get_effective_paths(m1)))
        self.assertEqual({m23}, self.dynamic_system._get_effective_paths(m2))

    def test_get_affected_models_and_its_inputs(self):
        """Should get the affected models and its inputs"""
        m1 = ModelMock(self.dynamic_system)
        m2 = ModelMock(self.dynamic_system)
        m3 = ModelMock(self.dynamic_system)

        m12 = Path(m1, m2, ExpressionProperty(Value(1)))
        m13 = Path(m1, m3, ExpressionProperty(Value(1)))
        m23 = Path(m2, m3, ExpressionProperty(Value(1)))

        np.random.seed(42)

        self.dynamic_system.link(m12)
        self.dynamic_system.link(m13)
        self.dynamic_system.link(m23)

        m1.get_output = lambda: 5
        m2.get_output = lambda: 15
        m3.get_output = lambda: 25

        self.dynamic_system.schedule(m1, Decimal(10))
        self.dynamic_system.schedule(m2, Decimal(10))
        self.dynamic_system.schedule(m3, Decimal(10))

        self.dynamic_system.get_output()

        (
            affected_models,
            inputs,
        ) = self.dynamic_system._get_affected_models_and_its_inputs()

        self.assertEqual({m2, m3}, affected_models)
        self.assertDictEqual(
            {m2: {m1.get_id(): 5}, m3: {m1.get_id(): 5, m2.get_id(): 15}}, inputs
        )


if __name__ == "__main__":
    unittest.main()
