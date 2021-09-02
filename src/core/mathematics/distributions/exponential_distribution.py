from __future__ import annotations

from decimal import Decimal

from core.config import FLOATING_POINT_DIGITS
from core.mathematics.distributions.random_distribution import RandomDistribution
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

    def generate(self) -> Decimal:
        """Generates a value following the distribution"""
        return Decimal(str(np.random.exponential(self.__mean))[:FLOATING_POINT_DIGITS])

    def generate_list(self, size: int) -> np.ndarray:
        """Generates a ndarray of values following the distribution

        Args:
            size (int): Size of the list
        """
        return np.random.exponential(self.__mean, size)

    def evaluate(self) -> Decimal:
        """Evaluates the expression"""
        return self.generate()

    def __str__(self):
        return super().__str__() + ".Exponential(" + str(self.__mean) + ")"
