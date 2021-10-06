"""Expressions module
=============================
Contains the abstract definition of Expression.
An expression is an abstract data type of the framework that admits any value that can be evaluated.

Example:
    Creating an expression::

        class Function(Expression):
            _x: float
            _b: float
            _m: float

            def __int__(self, x: float, b: float, m: float):
                self._x = x
                self._y = y
                self._m = m

            def evaluate(self):
                return self._x * self,_m + self._b
"""

from __future__ import annotations
from abc import abstractmethod


class Expression:
    """Property that can be evaluated"""

    @abstractmethod
    def evaluate(self):
        """Evaluates the expression"""
        raise NotImplementedError
