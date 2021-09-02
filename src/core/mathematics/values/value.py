from __future__ import annotations

from typing import Generic, TypeVar

from core.expresions.expression import Expression

T = TypeVar("T")


class Value(Expression, Generic[T]):
    __value: T

    def __init__(self, value: T):
        self.value = value

    def evaluate(self) -> T:
        return self.value

    def __str__(self):
        return str(self.evaluate())
