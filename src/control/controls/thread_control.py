from __future__ import annotations

from threading import Thread

from control.core import SimulationStrategy

from typing import Callable

from core.types import Time


class ThreadControlStrategy(SimulationStrategy):
    """Control that executes the simulation in a new thread"""

    _thread: Thread
    """Thread of the simulation"""

    def stop_simulation(self):
        self._thread = None

    def start_simulation(self, target: Callable, frequency: Time = 0, wait_time: Time = 0, stop_time: Time = 0):
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
        self._thread.join(timeout)
