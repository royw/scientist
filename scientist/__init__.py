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
        with Science('description') as experiment:
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
__docformat__ = 'restructuredtext en'

__version__ = '0.0.1'
