from __future__ import annotations

from abc import abstractmethod

from gsf.core.entity.core.entity import Entity


class EntityEmitter:
    """Emitter of new entities"""

    @abstractmethod
    def generate(self) -> Entity:
        """Generates an entity"""
        raise NotImplementedError
