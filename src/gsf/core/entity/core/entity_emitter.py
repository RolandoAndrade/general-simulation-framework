"""Entity Emitter
=============================
This module contains the definition of entity emitters.
It has the abstract definition of EntityEmitter that defines an abstract method to generate entities.

Example:
    Creating an entity emitter::

        class NewEntityEmitter(EntityEmitter):

            _count: int = 0

            def generate(self) -> Entity:
                self._count += 1
                return Model(str(count))
"""

from __future__ import annotations

from abc import abstractmethod

from gsf.core.entity.core.entity import Entity


class EntityEmitter:
    """Emitter of new entities"""

    @abstractmethod
    def generate(self) -> Entity:
        """Generates an entity"""
        raise NotImplementedError
