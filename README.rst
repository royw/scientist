
scientist
=========

Adapted to python from the github article at http://githubengineering.com/scientist/

Usage
-----

::

    def original(**kwargs):
        return foo(**kwargs)

    def trial(**kwargs):
        return bar(**kwargs)

    with Science('description') as experiment:
        experiment.use_function = original
        experiment.try_function = trial
        experiment.perform(user='me', password='sekret')

    print(Report.summary())



Installation
------------

To install from PyPI::

    ➤ pip install scientist


