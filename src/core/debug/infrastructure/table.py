from __future__ import annotations

from typing import Any, List

from prettytable import PrettyTable

from core.debug.domain.summary_table import SummaryTable


class Table(SummaryTable):
    _table: PrettyTable

    def __init__(self):
        self._table = PrettyTable()

    def build(self) -> str:
        return str(self._table)

    def addRow(self, row: List[Any]) -> Table:
        self._table.add_row(row)
        return self

    def setTitle(self, title: str) -> Table:
        self._table.title = title
        return self

    def setLabels(self, labels: List[str]) -> Table:
        self._table.field_names = labels
        return self

    def setAlignment(self, align: List[str]) -> SummaryTable:
        for field, alignment in zip(self._table.field_names, align):
            self._table.align[field] = alignment
        return self
