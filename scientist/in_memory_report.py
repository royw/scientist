# coding=utf-8

"""
Handle an experiment's report.
"""
from textwrap import dedent

from scientist.report import Report

__docformat__ = 'restructuredtext en'
__all__ = ('InMemoryReport',)


class InMemoryReport(Report):
    def __init__(self, description):
        super(InMemoryReport, self).__init__(description)
        self.experiments = []
        self.control_count = 0
        self.enabled_experiments = []
        self.enabled_count = 0
        self.contrary_experiments = []
        self.contrary_results = 0
        self.control_elapse_times = []
        self.control_avg_time = 0
        self.trial_elapse_times = []
        self.trial_avg_time = 0
        self.statuses = {}

    def __str__(self):
        """
        :return: The report string for this Report instance
        :rtype: str
        """
        output = [dedent("""
        {description}
        {hr}
        Total experiments: {control_count}
        Enabled experiments: {enabled_count}
        Contrary results: {contrary_results}
        Average time for control code: {control_avg_time}
        Average time for trial code: {trial_avg_time}
        Statuses: {statuses}
        """.format(hr='-' * len(self.description), **self.__dict__))]
        if self.contrary_experiments:
            output.append("Contrary Results:")
            for experiment in self.contrary_experiments:
                output.append("control value: " + repr(experiment.control.value))
                output.append("trial value: " + repr(experiment.trial.value))
                if experiment.control.cleaned_value is not None:
                    output.append("control cleaned value: " + repr(experiment.control.cleaned_value))
                if experiment.trial.cleaned_value is not None:
                    output.append("trial cleaned value: " + repr(experiment.trial.cleaned_value))
                output.append("")
        return "\n".join(output)

    def append(self, experiment):
        """
        Append an experiment instance to this report's list of experiments.

        :param experiment: the completed experiment instance
        :type experiment: Experiment
        """
        self.experiments.append(experiment)

    def summarize(self):
        """
        Calculate the report values for this Report instance.
        """
        self.control_count = len(self.experiments)
        self.enabled_experiments = [experiment for experiment in self.experiments if experiment.is_enabled]
        self.enabled_count = len(self.enabled_experiments)
        self.contrary_experiments = [experiment for experiment in self.enabled_experiments
                                     if experiment.status == 'contrite']
        self.contrary_results = len(self.contrary_experiments)

        def elapsed(start, end):
            return end - start

        self.control_elapse_times = [elapsed(experiment.control.start_time, experiment.control.end_time) for experiment
                                     in self.enabled_experiments]
        self.control_avg_time = sum(self.control_elapse_times) / float(len(self.control_elapse_times))

        self.trial_elapse_times = [elapsed(experiment.trial.start_time, experiment.trial.end_time) for experiment in
                                   self.enabled_experiments]
        self.trial_avg_time = sum(self.trial_elapse_times) / float(len(self.trial_elapse_times))
        self.statuses = {}
        for experiment in self.experiments:
            if experiment.status not in self.statuses:
                self.statuses[experiment.status] = 0
            self.statuses[experiment.status] += 1
