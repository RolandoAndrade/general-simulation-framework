"""Summary Table
=====================
This module contains the abstract definition of SummaryTable
that allows to create summary or report tables .

Example:
    Creating a summary table::

        class ReportTable(SummaryTable):
            _table: PrettyTable

            def __init__(self):
                self._table = PrettyTable()

            def build(self) -> str:
                return str(self._table)

            def add_row(self, row: List[Any]) -> Table:
                self._table.add_row(row)
                return self

            def set_title(self, title: str) -> Table:
                self._table.title = title
                return self

            def set_labels(self, labels: List[str]) -> Table:
                self._table.field_names = labels
                return self

            def set_alignment(self, align: List[str]) -> SummaryTable:
                for field, alignment in zip(self._table.field_names, align):
                    self._table.align[field] = alignment
                return self
"""


from __future__ import annotations

from abc import abstractmethod
from typing import Any, List


class SummaryTable:
    """Summary Table

    Abstract definition of tables that will be used by the framework.
    """

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
