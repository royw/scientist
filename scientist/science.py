# coding=utf-8

"""
Context for experimentally using new code
"""

from scientist.experiment import Experiment
from scientist.report import Report

__docformat__ = 'restructuredtext en'
__author__ = 'wrighroy'


class Science(object):
    """
    Context manager for running experiments.

    Note you may override the Report and Experiment classes used either at the class level or
    for the instance.

    Usage::

        with Science('description') as experiment:
            experiment.control_function = original
            experiment.trial_function = trial
            control_result = experiment.perform(user='me', password='sekret')

    """
    report = Report
    experiment = Experiment

    def __init__(self, description="Default Science Experiment", experiment=None, report=None):
        self.description = description
        self.experiment = experiment or Science.experiment
        self.report = report or Science.report
        self.__experiment = None

    def __enter__(self):
        self.__experiment = self.experiment(description=self.description, report=self.report)
        return self.__experiment

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__experiment is not None:
            self.__experiment.close()
        # returning false causes any exception raised during the context to be raised on context exit.
        return False

