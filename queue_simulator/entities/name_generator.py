from typing import Union

from core.entity.core import EntityManager
from queue_simulator.entities.available_entities import AvailableEntities
from queue_simulator.shared.nodes.node_types import NodeType


class NameGenerator(EntityManager):
    _source_serial: int
    _server_serial: int
    _sink_serial: int
    _path_serial: int
    _entity_serial: int
    _emitter_serial: int

    def __init__(self):
        super().__init__()
        self._source_serial = 0
        self._server_serial = 0
        self._sink_serial = 0
        self._path_serial = 0
        self._entity_serial = 0
        self._emitter_serial = 0

    def next_source(self) -> int:
        self._source_serial += 1
        return self._source_serial

    def next_server(self) -> int:
        self._server_serial += 1
        return self._server_serial

    def next_sink(self) -> int:
        self._sink_serial += 1
        return self._sink_serial

    def next_path(self) -> int:
        self._path_serial += 1
        return self._path_serial

    def next_entity(self) -> int:
        self._entity_serial += 1
        return self._entity_serial

    def next_emitter(self) -> int:
        self._emitter_serial += 1
        return self._emitter_serial

    def get_name(self, entity: Union[AvailableEntities, NodeType]):
        name_selector = {
            AvailableEntities.SOURCE: self.next_source,
            AvailableEntities.SERVER: self.next_server,
            AvailableEntities.SINK: self.next_sink,
            AvailableEntities.PATH: self.next_path,
            AvailableEntities.ENTITY_EMITTER: self.next_emitter,
            AvailableEntities.ENTITY: self.next_entity
        }
        return entity.capitalize() + str(name_selector[entity]())
