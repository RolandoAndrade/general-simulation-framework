from __future__ import annotations

from abc import ABC
from threading import Thread

from control.core.base_control import BaseControl

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.base_simulator import BaseSimulator


class ThreadControl(BaseControl, ABC):
    _thread: Thread

    def __init__(self, simulator: BaseSimulator):
        BaseControl.__init__(self, simulator)
        self._thread = Thread(target=self._execute)
