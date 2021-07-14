from __future__ import annotations

from abc import abstractmethod

from core.components.entity.core.entity import Entity
from core.components.expresions.expression import Expression


class EntityEmitter(Expression):
    """Emitter of new entities"""

    @abstractmethod
    def generate(self) -> Entity:
        """Generates an entity"""
        raise NotImplementedError

    def evaluate(self) -> EntityEmitter:
        """Evaluates the expression"""
        return self
