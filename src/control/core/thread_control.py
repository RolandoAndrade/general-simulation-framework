from __future__ import annotations

from abc import ABC
from threading import Thread

from control.core.base_control import BaseControl

from typing import TYPE_CHECKING

from core.events import EventBus
from core.types import Time

if TYPE_CHECKING:
    from simulation.core.base_simulator import BaseSimulator


class ThreadControl(BaseControl, ABC):
    """Control that executes the simulation in a new thread"""

    _thread: Thread
    """Thread of the simulation"""

    def __init__(self, simulator: BaseSimulator, event_bus: EventBus = None):
        BaseControl.__init__(self, simulator, event_bus)
        self._thread = Thread(target=self._execute)

    def _start_thread(
        self, frequency: Time = 0, wait_time: Time = 0, stop_time: Time = 0
    ):
        self._thread = Thread(
            target=self._execute,
            args=(
                frequency,
                wait_time,
                stop_time,
            ),
        )
        self._thread.start()

    def wait(self, timeout: Time = None):
        self._thread.join(timeout)
