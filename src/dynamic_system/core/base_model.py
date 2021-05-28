from __future__ import annotations

from abc import abstractmethod

from core.components.entity import Entity
from core.debug.domain.debug import debug


class BaseModel(Entity):
    """"DiscreteEventModel in a dynamic system"""
    _serial_id = 0

    @debug("Initialized Model", True)
    def __init__(self, name: str = None):
        if name is None:
            self.setID('model' + str(BaseModel._serial_id))
            BaseModel._serial_id = BaseModel._serial_id + 1
        else:
            self.setID(name)

    @abstractmethod
    def summary(self):
        """Prints a summary of the model"""
        pass
