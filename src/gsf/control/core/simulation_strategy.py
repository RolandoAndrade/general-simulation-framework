"""Simulation Control Strategy
==============
This module contains the abstract definition of a simulation control strategy.
It has the definition of the SimulationStrategy, that should be extended,
implementing its abstract methods.

Example:
    Creating an strategy::

        class NewStrategy(SimulationStrategy):
                def start_simulation(self, callable: Callable):
                    callable()

                def wait_simulation(self):
                    sleep(1)

                def stop_simulation(self):
                    return True
"""

from abc import ABC


class SimulationStrategy(ABC):
    """Defines a simulation strategy."""

    def start_simulation(self, *args, **kwargs):
        """Start the simulation."""
        raise NotImplementedError

    def wait_simulation(self, *args, **kwargs):
        """Waits the simulation."""
        raise NotImplementedError

    def stop_simulation(self, *args, **kwargs):
        """Stops the simulation."""
        raise NotImplementedError
