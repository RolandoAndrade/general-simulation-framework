from typing import Set, Dict

from core.debug.infrastructure.providers import TableProvider
from reports.core.base_report import BaseReport, Time, DynamicSystemOutput, ReportResult


class DefaultReport(BaseReport):
    def _get_results(
        self, headers: Set[str], outputs: Dict[Time, DynamicSystemOutput]
    ) -> ReportResult:
        x = TableProvider()
        x.set_labels(["time"] + list(headers)).set_title("Simulation report")
        for time in outputs:
            row = [time]
            for model in headers:
                if model in outputs[time]:
                    row += [outputs[time][model]]
                else:
                    row += ["-"]
            x.add_row(row)
        return x.build()
