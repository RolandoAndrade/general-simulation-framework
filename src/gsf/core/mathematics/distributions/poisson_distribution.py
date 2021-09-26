from __future__ import annotations

from gsf.core.mathematics.distributions.random_distribution import RandomDistribution
import numpy as np


class PoissonDistribution(RandomDistribution):
    """Draw samples from a Poisson distribution."""

    __mean: float
    """Mean of the distribution."""

    def __init__(self, mean: float):
        """Creates a poisson distribution

        Args:
            mean (float): Mean of the distribution.
        """
        self.__mean = mean

    def generate(self) -> int:
        """Generates a value following the distribution"""
        return np.random.poisson(self.__mean)

    def generate_list(self, size: int) -> np.ndarray:
        """Generates a ndarray of values following the distribution

        Args:
            size (int): Size of the list
        """
        return np.random.poisson(self.__mean, size)

    def evaluate(self) -> int:
        """Evaluates the expression"""
        return self.generate()

    def __str__(self):
        return super().__str__() + ".Poisson(" + str(self.__mean) + ")"
