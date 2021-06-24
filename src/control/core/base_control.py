from __future__ import annotations

from abc import abstractmethod

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from models.models.discrete_event_model import ModelInput
    from simulation.core.base_simulator import BaseSimulator


class BaseControl:
    _simulator: BaseSimulator
    _isPaused: bool

    def __init__(self, simulator: BaseSimulator):
        self._simulator = simulator
        self._isPaused = True

    @abstractmethod
    def _execute(self, frequency: float = 0, wait_time: float = 0):
        """
        Executes the simulation loop
        Args:
            frequency: Frequency of the simulation computation.
            wait_time: Delay execution for a given number of seconds.
        """
        raise NotImplementedError

    @abstractmethod
    def start(self, start_input: Dict[str, ModelInput] = None, frequency: float = 0, wait_time: float = 0):
        """
        Starts the simulation
        Args:
            start_input (Dict[str, ModelInput]): input
            frequency: Frequency of the simulation computation.
            wait_time: Delay execution for a given number of seconds.
        """
        raise NotImplementedError

    @abstractmethod
    def pause(self):
        """Pauses the simulation"""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stops the simulation"""
        raise NotImplementedError
