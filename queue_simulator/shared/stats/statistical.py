from abc import abstractmethod, ABC

from queue_simulator.shared.stats.component_stats import ComponentStats


class Statistical(ABC):
    """Get stats interface."""

    @abstractmethod
    def get_stats(self) -> ComponentStats:
        """Get the stats of the component."""
        raise NotImplementedError
