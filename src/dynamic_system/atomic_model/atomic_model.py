from __future__ import annotations
from abc import abstractmethod
from typing import Set, TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_model.value import Value

from dynamic_system.base_model import BaseModel


class AtomicModel(BaseModel):
    _variables: Set[Value]

    """Implements the state transition function
    :param bag_xb: set of bags with elements in X (inputs set)
    """

    @abstractmethod
    def delta(self, bag_xb: Set[Value]):
        pass

    """Implements the output function
    :param bag_yb: set of bags with elements in Y (outputs set)
    """

    @abstractmethod
    def output_function(self, bag_yb: Set[Value]):
        pass

    """Clear the allocated objects used for """

    @abstractmethod
    def garbage_collector_output(self):
        """"This is necessary because the model that created the object cannot know
        when the simulator is finished with it."""
        pass
