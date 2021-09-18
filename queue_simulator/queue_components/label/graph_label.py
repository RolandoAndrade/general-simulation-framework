from typing import Dict, Any

from core.entity.core import EntityProperties, Entity
from core.entity.properties import ExpressionProperty, StringProperty
from core.expresions import UserExpression
from queue_simulator.queue_components.entities import NameGenerator
from queue_simulator.queue_components.label.label import Label
from queue_simulator.queue_components.shared.expressions import ExpressionManager
from queue_simulator.queue_components.shared.models import SimulatorComponent


class GraphLabel(Label, SimulatorComponent):
    expression_property: ExpressionProperty

    def __init__(self, name: str, entity_manager: NameGenerator = None, expression_manager: ExpressionManager = None):
        Label.__init__(self, expression_manager=expression_manager)
        SimulatorComponent.__init__(self, name, entity_manager)
        self.expression_property = None

    def get_expressions(self) -> Dict[str, Any]:
        return {}

    def get_properties(self) -> EntityProperties:
        return {
            'Expression': self.expression_property or ''
        }

    def set_expression(self, expression: str):
        super().set_expression(expression)
        if self.expression_property is not None:
            self.expression_property.set_value(UserExpression(expression))
        else:
            self.expression_property = ExpressionProperty(UserExpression(expression))

