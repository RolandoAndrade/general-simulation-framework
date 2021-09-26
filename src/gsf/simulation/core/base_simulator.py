from __future__ import annotations

from abc import abstractmethod

from gsf.core.events import EventBus, static_event_bus
from gsf.dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
from gsf.reports.core.base_report import BaseReport


class BaseSimulator:
    """Abstract simulator engine.

    An simulator engine executes the state transition function of the dynamic
    system, computes the output and reports it.
    """

    _dynamic_system: BaseDynamicSystem
    """Dynamic system to be simulated."""

    _is_output_up_to_update: bool
    """Indicates if the output was computed for that iteration."""

    _report_generator: BaseReport
    """Current report generator where engine saves the outputs."""

    _event_bus: EventBus
    """Event bus of the module."""

    def __init__(
        self,
        dynamic_system: BaseDynamicSystem,
        base_generator: BaseReport,
        event_bus: EventBus = None,
    ):
        """
        Args:
            dynamic_system (BaseDynamicSystem): Dynamic system to be simulated.
            base_generator (BaseReport): Current report generator where engine saves the outputs.
            event_bus (EventBus): Event bus for domain events.
        """
        self._dynamic_system = dynamic_system
        self._is_output_up_to_update = False
        self._report_generator = base_generator
        self._event_bus = event_bus or static_event_bus

    @abstractmethod
    def compute_next_state(self, *args, **kwargs):
        """Compute the next state of the dynamic system.

        Args:
            *args:
            **kwargs:
        """
        raise NotImplementedError

    @abstractmethod
    def compute_output(self):
        """Compute the output of the dynamic system if it has not computed
        yet
        """
        raise NotImplementedError

    def init(self):
        self._is_output_up_to_update = False
