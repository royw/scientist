# coding=utf-8

"""
Experiment for using old function and trying new function simultaneously.
"""

import time

from scientist.report import Report

__docformat__ = 'restructuredtext en'
__author__ = 'wrighroy'


class Experiment(object):
    report = Report

    def __init__(self, description, report=None):
        self.description = description
        self.report = report or Experiment.report
        self.use_function = None
        self.use_result = None
        self.use_exception = None
        self.use_start_time = None
        self.use_end_time = None
        self.try_function = None
        self.try_result = None
        self.try_exception = None
        self.try_start_time = None
        self.try_end_time = None
        self.is_enabled = False
        self.context = {}

    # noinspection PyMethodMayBeStatic
    def enabled(self):
        """
        Is the experiment enabled?
        Override if you want it enabled only part of the time.

        :return: asserted if enabled
        :rtype: bool
        """
        return True

    def perform(self, **kwargs):
        self.context = dict(kwargs)
        try:
            self.use_start_time = time.time()
            self.use_result = self.use_function(**kwargs)
        except Exception as ex:
            self.use_exception = ex
        finally:
            self.use_end_time = time.time()

        self.is_enabled = self.enabled()
        if self.is_enabled:
            try:
                self.try_start_time = time.time()
                self.try_result = self.try_function(**kwargs)
            except Exception as ex:
                self.try_exception = ex
            finally:
                self.try_end_time = time.time()

        if self.report is not None:
            self.report.add(self)

        if self.use_exception is not None:
            raise self.use_exception
        return self.use_result

    def close(self):
        pass
