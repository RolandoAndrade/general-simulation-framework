from abc import ABC, abstractmethod
from typing import List, Any, Dict

from core.entity.core import Entity
from core.entity.core.property_type import PropertyType
from core.entity.properties import NumberProperty
from core.expresions import UserExpression
from queue_simulator.queue_components.shared.expressions import ExpressionManager
from queue_simulator.queue_components.shared.models.node_property import NodeProperty


class SimulatorComponent(ABC, Entity):
    def serialize(self) -> List[Dict[str, Any]]:
        properties = self.get_properties()
        e = [
            NodeProperty(
                "Name", self.get_id(), PropertyType.STRING, "Generic"
            ).serialize()
        ]
        for i in properties:
            e.append(
                NodeProperty(
                    i,
                    str(properties[i].get_value()),
                    str(properties[i].get_type()),
                    properties[i].get_category(),
                ).serialize()
            )
        return e

    def _value_string_property(self, value: str, expression_manager: ExpressionManager):
        return value

    def _value_expression(self, value: str, expression_manager: ExpressionManager):
        return expression_manager.get_expression(value)

    def _value_number(self, value: str, expression_manager: ExpressionManager):
        return eval(value)

    def set_serialized_property(self, serialized_property: NodeProperty, expression_manager: ExpressionManager):
        if serialized_property.property_name == "Name":
            self.set_id(serialized_property.property_value)
        else:
            edited_property = self.get_properties()[serialized_property.property_name]
            effect = {
                PropertyType.STRING: self._value_string_property,
                PropertyType.EXPRESSION: self._value_expression,
                PropertyType.NUMBER: self._value_number
            }
            method = effect[serialized_property.property_type]
            value = serialized_property.property_value
            new_property = method(value, expression_manager)
            edited_property.set_value(new_property)

    @abstractmethod
    def get_expressions(self) -> Dict[str, Any]:
        raise NotImplementedError
