"""Domain Events
=============================
This module contains the definition of the available domain events that are emitted by the simulation
framework.
"""

import enum


class DomainEvents(str, enum.Enum):
    """Contains the constants of the emitted events."""

    SIMULATION_STATUS = "SIMULATION_STATUS"
    """Emitted when the status of the simulation change after every iteration."""

    OUTPUT_SAVED = "OUTPUT_SAVED"
    """Emitted when an output is saved in the reports module."""

    SIMULATION_FINISHED = "SIMULATION_FINISHED"
    """Emitted when simulation is finished."""

    SIMULATION_STOPPED = "SIMULATION_STOPPED"
    """Emitted when simulation was stopped."""

    SIMULATION_PAUSED = "SIMULATION_PAUSED"
    """Emitted when simulation was paused."""
