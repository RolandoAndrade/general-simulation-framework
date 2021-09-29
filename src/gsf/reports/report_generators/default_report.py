"""Default Report
=============================
This module contains the definition of a simulation report.
It has the definition of the DefaultReport that generates simulation reports in a table format using PrettyTable

Example:
    Creating a default report::

        report = DefaultReport()

    Saving an output::

        report.add_output({model: model_output}, 1)

    Generating report::

        report.generate_report()
"""

from typing import Set, Dict

from gsf.core.debug.infrastructure.providers import TableProvider
from gsf.reports.core.base_report import (
    BaseReport,
    Time,
    DynamicSystemOutput,
)


class DefaultReport(BaseReport):
    """Default Report

    Creates a report table from the given outputs.
    """

    def _get_results(
        self, headers: Set[str], outputs: Dict[Time, DynamicSystemOutput]
    ) -> str:
        """Creates an str by applying a table format"""
        x = TableProvider()
        x.set_labels(["time"] + list(headers)).set_title("Simulation report")
        for time in outputs:
            row = [time]
            for model in headers:
                if model in outputs[time]:
                    if isinstance(outputs[time][model], list):
                        row += [[str(i) for i in outputs[time][model]]]
                    else:
                        row += [outputs[time][model]]
                else:
                    row += ["-"]
            x.add_row(row)
        return x.build()
