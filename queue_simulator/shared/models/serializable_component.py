from abc import ABC
from typing import List, Any, Dict

from core.entity.core import Entity
from core.entity.core.property_type import PropertyType
from queue_simulator.shared.models.node_property import NodeProperty


class SerializableComponent(ABC, Entity):
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

    def _value_string_property(self, value: str):
        return value

    def _value_expression(self, value: str):
        return value

    def set_serialized_property(self, serialized_property: NodeProperty):
        edited_property = self.get_properties()[serialized_property.property_name]
        effect = {
            PropertyType.STRING: self._value_string_property,
            PropertyType.EXPRESSION: self._value_expression
        }
        method = effect[serialized_property.property_type]
        value = serialized_property.property_value
        edited_property.set_value(method(value))
