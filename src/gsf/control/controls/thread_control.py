"""Thread Control Strategy
===========================
This module contains the definition of a simulation control strategy.
It has the definition of the ThreadControlStrategy, that allows control simulations using the library
threading.

Example:
    Using the strategy::

        ...
        dynamic_system = some_discrete_event_dynamic_system
        simulator = DiscreteEventSimulationEngine(dynamic_system, DefaultReport())
        simulation_strategy = ThreadControl()
        event_control = DiscreteEventControl(simulator, simulation_strategy)
"""

from __future__ import annotations

from threading import Thread

from gsf.control.core import SimulationStrategy

from typing import Callable

from gsf.core.types import Time


class ThreadControlStrategy(SimulationStrategy):
    """Strategy that executes the simulation in a new thread

    Attributes:
        _thread (Thread): Current thread of the simulation.
    """

    _thread: Thread
    """Thread of the simulation"""

    def stop_simulation(self):
        """Deletes the simulation thread."""
        self._thread = None

    def start_simulation(
        self,
        target: Callable,
        frequency: Time = 0,
        wait_time: Time = 0,
        stop_time: Time = 0,
    ):
        """Creates a new simulation thread with the specified target.

        Args:
            target (Callable): Method to be called to run the simulation.
            frequency (Time): Frequency of the simulation computation.
            wait_time (Time): Delay execution for a given.
            stop_time (Time): Duration of the simulation.
        """
        self._thread = Thread(
            target=target,
            args=(
                frequency,
                wait_time,
                stop_time,
            ),
        )
        self._thread.start()

    def wait_simulation(self, timeout: Time = None):
        """Merges the created thread to the main thread.

        Args:
            timeout (Time): time to merge.
        """
        self._thread.join(timeout)
