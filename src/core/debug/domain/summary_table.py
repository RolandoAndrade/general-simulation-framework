from __future__ import annotations

from abc import abstractmethod
from typing import Any, List


class SummaryTable:
    @abstractmethod
    def build(self) -> str:
        """Returns the table in string format"""
        pass

    @abstractmethod
    def addRow(self, row: List[Any]) -> SummaryTable:
        """Adds a row to the table"""
        pass

    @abstractmethod
    def setTitle(self, title: str) -> SummaryTable:
        """Sets the title of the table"""
        pass

    @abstractmethod
    def setLabels(self, labels: List[str]) -> SummaryTable:
        """Sets the labels of the table"""
        pass

    @abstractmethod
    def setAlignment(self, align: List[str]) -> SummaryTable:
        """Sets the alignment of the columns"""
        pass
