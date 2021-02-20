from typing import Set, TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_model.variable import Variable

from dynamic_system.base_model import BaseModel


class AtomicModel(BaseModel):

    _variables: Set[Variable]

    """Implements the state transition function"""

    def delta(self):
        pass

    """Implements the output function"""

    def output_function(self):
        pass
