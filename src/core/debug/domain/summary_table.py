from __future__ import annotations

from abc import abstractmethod
from typing import Any, List


class SummaryTable:
    @abstractmethod
    def build(self) -> str:
        """Returns the table in string format"""
        raise NotImplementedError

    @abstractmethod
    def add_row(self, row: List[Any]) -> SummaryTable:
        """Adds a row to the table

        Args:
            row: Row to be added.
        """
        raise NotImplementedError

    @abstractmethod
    def set_title(self, title: str) -> SummaryTable:
        """Sets the title of the table

        Args:
            title (str): Title of the table.
        """
        raise NotImplementedError

    @abstractmethod
    def set_labels(self, labels: List[str]) -> SummaryTable:
        """Sets the labels of the table

        Args:
            labels: Fields of the table.
        """
        raise NotImplementedError

    @abstractmethod
    def set_alignment(self, align: List[str]) -> SummaryTable:
        """Sets the alignment of the columns

        Args:
            align: Alignment of each column.
        """
        raise NotImplementedError
