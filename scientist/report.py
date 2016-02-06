# coding=utf-8

"""
Base class for reports that just provides the interface child classes should use.
"""
from itertools import tee, izip_longest
from textwrap import dedent

__docformat__ = 'restructuredtext en'
__all__ = ('Report',)


class Report(object):
    # reports are stored in a dictionary with the experiment's description as the key and a report instance as the
    # value.
    reports = {}
    report_divider = "-" * 78

    def __init__(self, description):
        self.description = description

    def __str__(self):
        """
        Child classes should override this method.

        :return: The report string for this Report instance
        :rtype: str
        """
        output = dedent("""
        {description}
        """.format(**self.__dict__))
        return output

    @classmethod
    def summary(cls):
        """
        :return: a report string for all of the Reports
        :rtype: str
        """
        parts = []
        for description in Report.reports.keys():
            report = Report.reports[description]
            report.summarize()
            parts.append(report)
            parts.append(Report.report_divider)
        return "\n".join(parts)

    @classmethod
    def get(cls, description):
        """
        Get the Report instance for the given description.  If description is None, then raise ValueError.

        :param description: the experiment's description.
        :type description: str
        :return: the report instance
        :rtype: Report
        """
        if description is None:
            raise ValueError("The description must not be None")

        if description not in Report.reports.keys():
            Report.reports[description] = cls(description)
        return Report.reports[description]

    @classmethod
    def add(cls, experiment):
        """
        Add an experiment instance to it's the report instance with the same description as the experiment.

        :param experiment: the completed experiment instance
        :type experiment: Experiment
        """
        report = cls.get(experiment.description)
        report.append(experiment)

    def append(self, experiment):
        """
        Append an experiment instance to this report's list of experiments.

        :param experiment: the completed experiment instance
        :type experiment: Experiment
        """
        # should be something like:
        # self.experiments.append(experiment)
        raise NotImplementedError()

    def summarize(self):
        """
        Calculate the report values for this Report instance.
        """
        raise NotImplementedError()
