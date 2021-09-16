from abc import abstractmethod, ABC

from queue_simulator.queue_components.shared.stats import DataSource


class StatSource(ABC):
    @abstractmethod
    def get_datasource(self) -> DataSource:
        """Get the stats of the component."""
        raise NotImplementedError
