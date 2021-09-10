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
