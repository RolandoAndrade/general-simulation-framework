from typing import Dict
from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from gsf.models.models import DiscreteTimeModel


class Cell(DiscreteTimeModel):
    """Cell of the Conway's Game of life

    It has an state alive or dead. When receives an input, changes its by the defined rules.
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
        values = inputs.values()
        count_alive = 0
        for is_alive in values:
            if is_alive:
                count_alive = count_alive + 1
        return (not state and count_alive == 3) or (state and 2 <= count_alive <= 3)

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
