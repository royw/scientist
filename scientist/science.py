# coding=utf-8

"""
Context for experimentally using new code
"""
from decorator import contextmanager

from scientist.experiment import Experiment
from scientist.report import Report

__docformat__ = 'restructuredtext en'
__author__ = 'wrighroy'


class Science(object):
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
        return False

