"""Table
=============================
This module contains the definition of a summary table.
It has the definition of the Table that creates a output with a table format provided by PrettyTable.

Example:
    Creating a table::

        table = Table()
"""


from __future__ import annotations

from typing import Any, List

from prettytable import PrettyTable

from gsf.core.debug.domain.summary_table import SummaryTable


class Table(SummaryTable):
    """Table

    Creates a table using Pretty Table

    Attributes:
        _table (PrettyTable): Created table.
    """

    _table: PrettyTable

    def __init__(self):
        self._table = PrettyTable()

    def build(self) -> str:
        """Returns the table in string format"""
        return str(self._table)

    def add_row(self, row: List[Any]) -> Table:
        """Adds a row to the table

        Args:
            row: Row to be added.
        """
        self._table.add_row(row)
        return self

    def set_title(self, title: str) -> Table:
        """Sets the title of the table

        Args:
            title (str): Title of the table.
        """
        self._table.title = title
        return self

    def set_labels(self, labels: List[str]) -> Table:
        """Sets the labels of the table

        Args:
            labels: Fields of the table.
        """
        self._table.field_names = labels
        return self

    def set_alignment(self, align: List[str]) -> SummaryTable:
        """Sets the alignment of the columns

        Args:
            align: Alignment of each column.
        """
        for field, alignment in zip(self._table.field_names, align):
            self._table.align[field] = alignment
        return self
