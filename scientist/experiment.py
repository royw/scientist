# coding=utf-8

"""
Experiment for using old function and trying new function simultaneously.
"""

import time

__docformat__ = 'restructuredtext en'
__all__ = ('Experiment',)


class Experiment(object):
    """
    An experiment consists of calling a control function and when enabled, a trial function.

    Information about the experiment is encapsulated as instance attributes.

    The experiment instance is then added to the Report system.

    To lower the duty cycle of when the trial function is executed, adjust the asserted duty
    cycle of the enabled method (ex: for 20% duty cycle, the enabled method should return rand(100) < 20).
    """
    def __init__(self, description, report=None):
        self.description = description
        self.report = report
        self.control_function = None
        self.control_result = None
        self.control_exception = None
        self.control_start_time = None
        self.control_end_time = None
        self.trial_function = None
        self.trial_result = None
        self.trial_exception = None
        self.trial_start_time = None
        self.trial_end_time = None
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
        """
        Perform the experiment by running the control function and, if enabled, the trial function.  Capture the
        results, any exceptions, and the start and end times.

        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        self.context = dict(kwargs)

        # run the control function

        try:
            self.control_start_time = time.time()
            self.control_result = self.control_function(**kwargs)
        except Exception as ex:
            self.control_exception = ex
        finally:
            self.control_end_time = time.time()

        # if enabled, run the trial function

        self.is_enabled = self.enabled()
        if self.is_enabled:
            try:
                self.trial_start_time = time.time()
                self.trial_result = self.trial_function(**kwargs)
            except Exception as ex:
                self.trial_exception = ex
            finally:
                self.trial_end_time = time.time()

        # add this experiment instance to the report
        if self.report is not None:
            self.report.add(self)

        # now return as the control function would have returned
        if self.control_exception is not None:
            raise self.control_exception
        return self.control_result

    def close(self):
        pass
