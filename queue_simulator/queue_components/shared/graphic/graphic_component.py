from __future__ import annotations
from queue_simulator.queue_components.shared.graphic import Point2D
from queue_simulator.queue_components.shared.models import SerializedComponent


class SerializedGraphicComponent(SerializedComponent):
    position: Point2D


class GraphicComponent:
    _position: Point2D

    def get_position(self) -> Point2D:
        return self._position

    def set_position(self, position: Point2D):
        self._position = position
