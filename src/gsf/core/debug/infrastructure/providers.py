"""Providers module
=============================
This module instances the concrete dependencies for the module.
"""

from typing import Type

from gsf.core.debug.domain.summary_table import SummaryTable
from gsf.core.debug.infrastructure.table import Table

TableProvider: Type[SummaryTable] = Table
"""Is the concrete instance of the summary table to be used by the framework."""
