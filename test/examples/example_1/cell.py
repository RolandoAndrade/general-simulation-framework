from typing import Dict
from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from gsf.models.models import DiscreteTimeModel


class Cell(DiscreteTimeModel):
    """Cell of the linear cellular automata

    It has an state alive or dead. When receives an input, changes its state to that input.
    Its output is the state.

    Attributes:
      _symbol (str): Symbol that represents the cell when it is printed in console.
    """

    _symbol: str

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        state: bool,
        symbol: str = None,
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Automata Grid where the cell belongs.
            state (bool); State that indicates whether the cell is alive (True) or dead (False).
            symbol (str): Symbol that represents the cell when it is printed in console.
        """
        super().__init__(dynamic_system, state=state)
        self._symbol = symbol or "\u2665"

    def _state_transition(self, state: bool, inputs: Dict[str, bool]) -> bool:
        """
        Receives an input and changes the state of the cell.
        Args:
            state (bool); Current state of the cell.
            inputs: A dictionary where the key is the input source cell and the value the output of that cell.

        Returns:
            The new state of the cell.
        """
        next_state: bool = list(inputs.values())[0]
        return next_state

    def _output_function(self, state: bool) -> bool:
        """
        Returns the state of the cell.
        """
        return state

    def __str__(self):
        """Prints the cell with the defined symbol"""
        is_alive = self.get_state()
        if is_alive:
            return self._symbol
        return "-"
