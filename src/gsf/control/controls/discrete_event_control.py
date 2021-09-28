"""Discrete Event Control
==============
This module contains the definition of a discrete event simulation control.
It has the definition of the DiscreteEventControl, that allows control simulations.

Example:
    Creating a discrete-event control::

        ...
        dynamic_system = some_discrete_event_dynamic_system
        simulator = DiscreteEventSimulationEngine(dynamic_system, DefaultReport())
        simulation_strategy = ThreadControl()
        event_control = DiscreteEventControl(simulator, simulation_strategy)

    Simulating a discrete-event simulation::

        event_control.start(stop_time=10)
"""


from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Dict

from gsf.control.core import SimulationStats, BaseControl, SimulationStrategy
from gsf.core.debug.domain.debug import debug
from gsf.core.events import EventBus, DomainEvents
from gsf.core.types import Time
from gsf.models.models.discrete_event_model import ModelInput

if TYPE_CHECKING:
    from gsf.simulation.simulation_engines.discrete_event_simulation_engine import (
        DiscreteEventSimulationEngine,
    )


class DiscreteEventControl(BaseControl):
    """Control that executes the discrete-event simulation

    Allows the control of discrete-event simulations,

    Attributes:
        _time (Time): current clock time of the simulation.
    """

    _simulator: DiscreteEventSimulationEngine
    """Overrides simulator type"""

    _time: Time
    """Current time of the simulation"""

    def __init__(
        self,
        simulator: DiscreteEventSimulationEngine,
        simulation_strategy: SimulationStrategy,
        event_bus: EventBus = None,
    ):
        """
        Args:
            simulator (DiscreteEventSimulationEngine): Simulation engine to be
                executed.
            simulation_strategy (SimulationStrategy): Strategy to execute the simulation.
            event_bus (EventBus): EvenBus of the module.
        """
        BaseControl.__init__(self, simulator, simulation_strategy, event_bus)
        self._time = Time(0)
        self._is_paused = False

    def _finish_simulation(self):
        """Finishes the simulation."""
        self._is_paused = True
        self._event_bus.emit(DomainEvents.SIMULATION_FINISHED)
        self.init()

    def _execute(self, frequency: Time, wait_time: Time, stop_time: Time):
        """Executes the simulation loop number of seconds.

        Args:
            frequency (Time): Frequency of the simulation computation.
            wait_time (Time): Delay execution for a given.
            stop_time (Time): Duration of the simulation.
        """
        while not self._is_paused:
            next_event_time = self._simulator.get_time_of_next_event()
            if next_event_time < 0:
                self._finish_simulation()
            next_time = min(self._time + min(next_event_time, frequency), stop_time)
            self.next_step(next_time)
            sleep(wait_time)
            if 0 <= stop_time <= self._time:
                self._finish_simulation()
            else:
                self._event_bus.emit(
                    DomainEvents.SIMULATION_STATUS,
                    SimulationStats(self._time, stop_time, frequency, self._is_paused),
                )

    def next_step(self, time: Time = None):
        """Executes the next step of the simulation

        Args:
            time (Time): time of the next step. If it is None, takes the time of the next event.
        """
        time = time or (self._time + self._simulator.get_time_of_next_event())
        self._time = time
        self._simulator.compute_next_state(time=self._time)
        return time

    @debug("Simulation starts")
    def start(
        self,
        start_input: Dict[str, ModelInput] = None,
        frequency: Time = Time(1000),
        stop_time: Time = 0,
        wait_time: Time = 0,
    ):
        """Starts the simulation

        Args:
            start_input: Input of the dynamic system.
            frequency (Time): Frequency of the simulation computation.
            stop_time (Time): Time of the simulation
            wait_time (Time): Delay execution for a given number of seconds.
        """
        self._is_paused = False
        if self._time == 0:
            self._simulator.compute_next_state(start_input)
        self._simulation_strategy.start_simulation(
            self._execute, frequency, wait_time, stop_time
        )

    @debug("Simulation paused")
    def pause(self):
        """Pauses the simulation"""
        self._event_bus.emit(DomainEvents.SIMULATION_PAUSED)
        self._is_paused = True

    @debug("Simulation ended")
    def stop(self):
        """Stops the simulation"""
        self._event_bus.emit(DomainEvents.SIMULATION_STOPPED)
        self._is_paused = True
        self._simulation_strategy.stop_simulation()
        self.init()

    def init(self):
        """Initializes the clock and the simulator."""
        self._time = Time(0)
        self._simulator.init()

    def wait(self, timeout: Time = None):
        """Waits for the simulation process.
        Args:
            timeout (Time): time to wait.
        """
        self._simulation_strategy.wait_simulation(timeout)

    @property
    def time(self):
        """Current clock time of the simulation"""
        return self._time
