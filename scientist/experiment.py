# coding=utf-8

"""
Experiment for using old function and trying new function simultaneously.
"""

import time
from itertools import tee, izip_longest

__docformat__ = 'restructuredtext en'
__all__ = ('Experiment',)


class Runner(object):
    def __init__(self):
        self.function = None
        self.value = None
        self.cleaned_value = None
        self.exception = None
        self.start_time = None
        self.end_time = None

    def execute(self, clean, **kwargs):
        try:
            self.start_time = time.time()
            self.value = self.function(**kwargs)
            if clean is not None:
                self.cleaned_value = clean(self.function(**kwargs))
        except Exception as ex:
            self.exception = ex
        finally:
            self.end_time = time.time()


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
        self.comparator = self.compare
        self.clean = None
        self.ignore = None
        self.control = Runner()
        self.trial = Runner()
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
        self.control.execute(clean=self.clean, **kwargs)

        # if enabled, run the trial function

        self.is_enabled = self.enabled()
        if self.is_enabled:
            self.before_run()
            self.trial.execute(clean=self.clean, **kwargs)

        # add this experiment instance to the report
        if self.report is not None:
            self.report.add(self)

        # now return as the control function would have returned
        if self.control.exception is not None:
            raise self.control.exception
        return self.control.value

    def close(self):
        pass

    # noinspection PyMethodMayBeStatic
    def before_run(self):
        """
        Only ran when the trail is enabled.

        Override for expensive setup for trail functions.
        """
        pass

    @staticmethod
    def compare(a, b):
        return a == b

    @staticmethod
    def compare_generators(gen_1, gen_2):
        gen_1, gen_1_teed = tee(gen_1)
        sentinel = object()
        return all(a == b for a, b in izip_longest(gen_1, gen_2, fillvalue=sentinel))
