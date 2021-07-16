from __future__ import annotations

from mathematics.distributions.random_distribution import RandomDistribution
import numpy as np


class ExponentialDistribution(RandomDistribution):
    """Draw samples from a Exponential distribution."""

    __mean: float
    """Mean of the distribution."""

    def __init__(self, mean: float):
        """Creates a Exponential distribution

        Args:
            mean (float): Mean of the distribution.
        """
        self.__mean = mean

    def generate(self) -> int:
        """Generates a value following the distribution"""
        return np.random.exponential(self.__mean)

    def generateList(self, size: int) -> np.ndarray:
        """Generates a ndarray of values following the distribution

        Args:
            size (int): Size of the list
        """
        return np.random.exponential(self.__mean, size)

    def evaluate(self) -> int:
        """Evaluates the expression"""
        return self.generate()
