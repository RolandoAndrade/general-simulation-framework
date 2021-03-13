from __future__ import annotations

from typing import Set


class BaseModel:
    """"Model in a dynamic system"""
    _id: str
    _serial_id = 0
    _savedNames: Set[str] = []

    def __init__(self, name: str = None):
        if name is None:
            self.setName('model' + str(BaseModel._serial_id))
            BaseModel._serial_id = BaseModel._serial_id + 1
        else:
            self.setName(name)

    def getID(self) -> str:
        """Returns the identifier of the model"""
        return self._id

    def setName(self, name: str):
        if name in BaseModel._savedNames:
            raise Exception('Name already taken')
        else:
            self._id = name

    def summary(self):
        """Print a summary of the model"""
        row_format = "{:>15}" * 5
        print(row_format.format("", *["ID", "TYPE", "NAME", "INPUTS", "OUTPUTS"]))
