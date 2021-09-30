"""Recovery Strategy
=====================
This module contains the abstract definition of a recovery strategy.
It has an abstract definition RecoveryStrategy that should be extended
implementing its abstract methods.

Example:
    Creating a recovery strategy::

        class PickleRecovery(RecoveryStrategy):
            def save(self, experiment: BaseExperiment, *args, **kwargs) -> bytes:
                return pickle.dumps(experiment)

            def load(self, data: bytes) -> BaseDynamicSystem:
                return pickle.loads(cast(Any, data))
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gsf.experiments.core.base_experiment import BaseExperiment


class RecoveryStrategy:
    """Recovery Strategy

    Determines how an experiment is saved and loaded.
    """
    @abstractmethod
    def save(self, experiment: BaseExperiment, *args, **kwargs):
        """Saves the experiment"""
        raise NotImplementedError

    @abstractmethod
    def load(self, *args, **kwargs) -> BaseExperiment:
        """Recovers a previous existing experiment."""
        raise NotImplementedError
