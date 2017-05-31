# coding=utf-8

"""
Scientist
=========

Adapted to python from the github article at http://githubengineering.com/scientist/

"use" in the article refers to the original code while "try" refers to the new code.  Because "try"
is a python reserved word and for clarity, we use the terms "control" for the original code and "trial"
for the new code.

Also python does not support returning a value from the "with" construct unlike ruby's "do" statement
so added a "perform" method to the Experiment class that returns the "control" method's results.  Also
instead of using a "context" method, the parameters for the "control" and "trial" methods are passed
to the "perform method" as kwargs.

Usage
-----

::

    def original(**kwargs):
        return foo(**kwargs)

    def trial(**kwargs):
        return bar(**kwargs)

    try:
        with Scientist('description') as experiment:
            experiment.control_function = original
            experiment.trial_function = trial
            control_result = experiment.perform(user='me', password='sekret')
    except Exception:
        # ad exception raised by the control_function
        pass

    print(Report.summary())



Installation
------------

To install from PyPI::

    ➤ pip install scientist


"""

from scientist.experiment import Experiment
from scientist.report import Report

__docformat__ = 'restructuredtext en'
__all__ = ('Scientist',)
__version__ = '0.0.5'


# To work around python's half-assed packaging scheme, the Scientist class is located here instead of in it's own file.
class Scientist(object):
    """
    Context manager for running experiments.

    Note you may override the Report and Experiment classes used either at the class level or
    for the instance.

    Usage::

        with Scientist('description') as experiment:
            experiment.control_function = original
            experiment.trial_function = trial
            control_result = experiment.perform(user='me', password='sekret')

    """
    report = Report
    experiment = Experiment

    def __init__(self, description="Default Scientist Experiment", experiment_=None, report_=None):
        self.description = description
        self.experiment = experiment_ or Scientist.experiment
        self.report = report_ or Scientist.report
        self.__experiment = None

    def __enter__(self):
        self.__experiment = self.experiment(description=self.description, report=self.report)
        return self.__experiment

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__experiment is not None:
            self.__experiment.close()
        # returning false causes any exception raised during the context to be raised on context exit.
        return False
