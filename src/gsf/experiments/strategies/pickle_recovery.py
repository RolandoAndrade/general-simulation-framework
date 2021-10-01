"""Recovery Strategy
=====================
This module contains the definition of a recovery strategy.
It has the definition of PickleStrategy that allows to save and import experiments
stored as a pickle file.

Example:
    Creating the strategy::

        strategy = PickleStrategy()
"""

from __future__ import annotations

from gsf.dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
from gsf.experiments.core.recovery_strategy import RecoveryStrategy

import pickle
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from gsf.experiments.core.base_experiment import BaseExperiment


class PickleRecovery(RecoveryStrategy):
    """Pickle Recovery Strategy

    It saves the experiments using the pickle serialization library.
    """

    def save(self, experiment: BaseExperiment, *args, **kwargs) -> bytes:
        """Saves the experiment"""
        return pickle.dumps(experiment)

    def load(self, data: bytes) -> BaseDynamicSystem:
        """Recovers a previous existing experiment."""
        return pickle.loads(cast(Any, data))
