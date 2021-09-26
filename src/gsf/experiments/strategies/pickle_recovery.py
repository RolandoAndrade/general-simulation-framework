from __future__ import annotations

from gsf.dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
from gsf.experiments.core.recovery_strategy import RecoveryStrategy

import pickle
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from gsf.experiments.core.base_experiment import BaseExperiment


class PickleRecovery(RecoveryStrategy):
    def save(self, experiment: BaseExperiment, *args, **kwargs) -> bytes:
        return pickle.dumps(experiment)

    def load(self, data: bytes) -> BaseDynamicSystem:
        return pickle.loads(cast(Any, data))
