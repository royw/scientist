# coding=utf-8

"""
Context for experimentally using new code
"""
from contextlib import contextmanager

from scientist.experiment import Experiment

__docformat__ = 'restructuredtext en'
__author__ = 'wrighroy'


# noinspection PyBroadException
@contextmanager
def Science(description="Default Science Experiment", experiment=Experiment):
    """
    Enable using Science using the *with* function.

    Usage::
        with Science() as experiment:
            experiment.foo(bar)

    :param description: description of this science experiment
    :type description: str
    :param experiment: override the experiment class, defaults to Experiment
    :type experiment: Experiment

    """
    obj = None
    try:
        obj = experiment(description)
        yield obj
    finally:
        try:
            if obj is not None:
                obj.close()
        except:
            pass
