from __future__ import annotations
from abc import abstractmethod


class Expression:
    """Property that can be evaluated"""

    @abstractmethod
    def evaluate(self):
        """Evaluates the expression"""
        raise NotImplementedError
