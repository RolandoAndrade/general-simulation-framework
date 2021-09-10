from __future__ import annotations

from decimal import Decimal

from core.config import FLOATING_POINT_DIGITS
from core.mathematics.distributions.random_distribution import RandomDistribution
import numpy as np


class TriangularDistribution(RandomDistribution):
    """Draw samples from a Triangular distribution."""

    __minimum: float
    """Mean of the distribution."""

    __mode: float
    """Mode of the distribution."""

    __maximum: float
    """Maximum of the distribution."""

    def __init__(self, minimum: float, mode: float, maximum: float):
        """Creates a Exponential distribution

        Args:
            minimum (float): Mean of the distribution.
            mode (float): Mode of the distribution.
            maximum (float): Maximum of the distribution.
        """
        self.__minimum = minimum
        self.__mode = mode
        self.__maximum = maximum

    def generate(self) -> Decimal:
        """Generates a value following the distribution"""
        return Decimal(
            str(np.random.triangular(self.__minimum, self.__mode, self.__maximum))[
                :FLOATING_POINT_DIGITS
            ]
        )

    def generate_list(self, size: int) -> np.ndarray:
        """Generates a ndarray of values following the distribution

        Args:
            size (int): Size of the list
        """
        return np.random.triangular(self.__minimum, self.__mode, self.__maximum, size)

    def evaluate(self) -> Decimal:
        """Evaluates the expression"""
        return self.generate()

    def __str__(self):
        return (
            super().__str__()
            + ".Triangular("
            + str(self.__minimum)
            + ", "
            + str(self.__mode)
            + ", "
            + str(self.__maximum)
            + ")"
        )
