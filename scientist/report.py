# coding=utf-8

"""
Handle an experiment's report.
"""
from textwrap import dedent

__docformat__ = 'restructuredtext en'
__author__ = 'wrighroy'

__all__ = ('Report',)

# reports are stored in a dictionary
reports = {}
report_divider = "-" * 78


class Report(object):
    def __init__(self, description):
        self.description = description
        self.experiments = []
        self.count = 0
        self.enabled_experiments = []
        self.tries = 0
        self.contrary_experiments = []
        self.contrary_results = 0
        self.use_elapse_times = []
        self.use_avg_time = 0
        self.try_elapse_times = []
        self.try_avg_time = 0

    def __str__(self):
        output = dedent("""
        {description}
        Total experiments: {count}
        Enabled experiments: {tries}
        Contrary results: {contrary_results}
        Average time for control code: {use_avg_time}
        Average time for trial code: {try_avg_time}
        """.format(**self.__dict__))
        if self.contrary_experiments:
            output += "\nContrary Results:\n"
            for experiment in self.contrary_experiments:
                output += "use results: " + repr(experiment.use_result) + "\n"
                output += "try results: " + repr(experiment.try_result) + "\n\n"
        return output

    @classmethod
    def summary(cls):
        parts = []
        for description in reports.keys():
            report = reports[description]
            report.summarize()
            parts.append(report)
            parts.append(report_divider)
        return "\n".join(parts)

    @classmethod
    def get(cls, description=None):
        if description is None:
            return reports

        if description not in reports.keys():
            reports[description] = Report(description)
        return reports[description]

    @classmethod
    def add(cls, experiment):
        report = Report.get(experiment.description)
        report.append(experiment)

    def append(self, experiment):
        self.experiments.append(experiment)

    def summarize(self):
        self.count = len(self.experiments)
        self.enabled_experiments = [experiment for experiment in self.experiments if experiment.is_enabled]
        self.tries = len(self.enabled_experiments)
        self.contrary_experiments = [experiment for experiment in self.enabled_experiments
                                     if
                                     experiment.use_result != experiment.try_result or
                                     experiment.use_exception != experiment.try_exception]
        self.contrary_results = len(self.contrary_experiments)

        def elapsed(start, end):
            return end - start

        self.use_elapse_times = [elapsed(experiment.use_start_time, experiment.use_end_time) for experiment in
                                 self.enabled_experiments]
        self.use_avg_time = sum(self.use_elapse_times) / float(len(self.use_elapse_times))

        self.try_elapse_times = [elapsed(experiment.try_start_time, experiment.try_end_time) for experiment in
                                 self.enabled_experiments]
        self.try_avg_time = sum(self.try_elapse_times) / float(len(self.try_elapse_times))
