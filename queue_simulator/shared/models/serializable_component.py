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
