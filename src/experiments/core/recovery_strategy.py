from __future__ import annotations

from abc import abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments.core.base_experiment import BaseExperiment


class RecoveryStrategy:
    @abstractmethod
    def save(self, experiment: BaseExperiment, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def load(self, *args, **kwargs) -> BaseExperiment:
        raise NotImplementedError
