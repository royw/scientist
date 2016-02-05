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

    def __str__(self):
        """
        :return: The report string for this Report instance
        :rtype: str
        """
        output = dedent("""
        {description}
        Total experiments: {control_count}
        Enabled experiments: {enabled_count}
        Contrary results: {contrary_results}
        Average time for control code: {control_avg_time}
        Average time for trial code: {trial_avg_time}
        """.format(**self.__dict__))
        if self.contrary_experiments:
            output += "\nContrary Results:\n"
            for experiment in self.contrary_experiments:
                output += "control results: " + repr(experiment.control_result) + "\n"
                output += "trial results: " + repr(experiment.trial_result) + "\n\n"
        return output

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
                                     if
                                     experiment.control_result != experiment.trial_result or
                                     experiment.control_exception != experiment.trial_exception]
        self.contrary_results = len(self.contrary_experiments)

        def elapsed(start, end):
            return end - start

        self.control_elapse_times = [elapsed(experiment.control_start_time, experiment.control_end_time) for experiment
                                     in self.enabled_experiments]
        self.control_avg_time = sum(self.control_elapse_times) / float(len(self.control_elapse_times))

        self.trial_elapse_times = [elapsed(experiment.trial_start_time, experiment.trial_end_time) for experiment in
                                   self.enabled_experiments]
        self.trial_avg_time = sum(self.trial_elapse_times) / float(len(self.trial_elapse_times))
