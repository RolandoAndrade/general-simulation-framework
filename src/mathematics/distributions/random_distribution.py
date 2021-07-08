from __future__ import annotations
from abc import abstractmethod
from typing import Union, List

from core.components.expresions.expression import Expression


class RandomDistribution(Expression):
    """Math random distribution"""

    @abstractmethod
    def generate(self) -> Union[float, int]:
        """Generates a value following the distribution"""
        raise NotImplementedError

    @abstractmethod
    def generateList(self, size: int) -> Union[List[float], List[int]]:
        """Generates a list of values following the distribution

        Args:
            size (int): Size of the list
        """
        raise NotImplementedError
