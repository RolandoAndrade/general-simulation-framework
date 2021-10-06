"""Random Distribution
=============================
Contains the abstract definition of a random distribution. It allows to create custom distributions
as expressions that can be used in the framework.

Example:
    Creating the distribution::

        class SomeRandomDistribution(RandomDistribution):
            _min: float

            def __init__(self, min: float):
                self._min = min

            def generate(self) -> float:
                raise random() + min

            def generate_list(self, size: int) -> List[float]:
                r = []
                for i in range(size):
                    r.append(self.generate())
                return r
"""

from __future__ import annotations
from abc import abstractmethod
from typing import Union, List

from gsf.core.expresions.expression import Expression


class RandomDistribution(Expression):
    """Math random distribution"""

    @abstractmethod
    def generate(self) -> Union[float, int]:
        """Generates a value following the distribution"""
        raise NotImplementedError

    @abstractmethod
    def generate_list(self, size: int) -> Union[List[float], List[int]]:
        """Generates a list of values following the distribution

        Args:
            size (int): Size of the list
        """
        raise NotImplementedError

    def __str__(self):
        return "Random"
