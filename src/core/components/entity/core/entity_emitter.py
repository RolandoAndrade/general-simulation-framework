from __future__ import annotations

from abc import abstractmethod

from core.components.entity.core.entity import Entity


class EntityEmitter:
    @abstractmethod
    def generate(self) -> Entity:
        raise NotImplementedError
