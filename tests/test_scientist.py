# coding=utf-8

"""
Using 2 different algorithms for calculating fibonacci sequence (from
http://stackoverflow.com/questions/494594/how-to-write-the-fibonacci-sequence-in-python)
as control and trial experiment.
"""
import sys

import scientist
from scientist.experiment import Experiment
from scientist.in_memory_report import InMemoryReport
from scientist import Scientist
from math import sqrt

__docformat__ = 'restructuredtext en'

Scientist.report = InMemoryReport

print("sys.path: {path}".format(path=sys.path))


def test_version():
    print("scientist-{ver}".format(ver=scientist.__version__))
    assert scientist.__version__


def f(n):
    return int(((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5)))


def SubFib(startNumber, endNumber):
    n = 0
    cur = f(n)
    while cur <= endNumber:
        if startNumber <= cur:
            yield cur
        n += 1
        cur = f(n)


def F():
    a, b = 0, 1
    yield a
    yield b
    while True:
        a, b = b, a + b
        yield b


def F_buggy():
    # a, b = 0, 1
    a, b = 1, 2  # intentional bug
    yield a
    yield b
    while True:
        a, b = b, a + b
        yield b


def NewSubFib(startNumber, endNumber):
    for cur in F():
        if cur > endNumber:
            return
        if cur >= startNumber:
            yield cur


def BuggySubFib(startNumber, endNumber):
    for cur in F_buggy():
        if cur > endNumber:
            return
        if cur >= startNumber:
            yield cur


def KaboomSubFib(startNumber, endNumber):
    for cur in F():
        if cur == 5:
            raise ValueError(cur)
        if cur > endNumber:
            return
        if cur >= startNumber:
            yield cur


def test_summary():
    # noinspection PyProtectedMember
    name = sys._getframe().f_code.co_name

    def original(**kwargs):
        return list(SubFib(**kwargs))

    def trial(**kwargs):
        return list(NewSubFib(**kwargs))

    for index in range(0, 2000, 100):
        with Scientist(name) as experiment:
            experiment.control.function = original
            experiment.trial.function = trial
            result = experiment.perform(startNumber=index, endNumber=3000 + index)
            assert result

    report = Scientist.report.get(name)
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 0
    assert str(report)


def test_summary_with_bug():
    # noinspection PyProtectedMember
    name = sys._getframe().f_code.co_name

    def original(**kwargs):
        return list(SubFib(**kwargs))

    def trial(**kwargs):
        return list(BuggySubFib(**kwargs))

    def first4(value_list):
        return value_list[0:4]

    for index in range(0, 2000, 100):
        with Scientist(name) as experiment:
            experiment.control.function = original
            experiment.trial.function = trial
            experiment.clean = first4
            experiment.perform(startNumber=index, endNumber=3000 + index)

    report = Scientist.report.get(name)
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 1
    assert str(report)
    assert report.statuses['match']
    assert report.statuses['contrite'] == 1


def test_lambda():
    # noinspection PyProtectedMember
    name = sys._getframe().f_code.co_name

    def ignore(**kwargs):
        return kwargs['startNumber'] % 1000 == 0

    for index in range(0, 200000, 100):
        with Scientist(name) as experiment:
            experiment.control.function = lambda **kwargs: SubFib(**kwargs)
            experiment.trial.function = lambda **kwargs: NewSubFib(**kwargs)
            # the lambdas here return generators so we need to tell the experiment to compare generates
            experiment.comparator = experiment.compare_generators
            # for grins, let's only run the trial a quarter of the time and ignore startNumbers on 1000 boundary
            experiment.duty_cycle = 25
            experiment.ignore = ignore
            # context gets combined with kwargs to perform()
            experiment.context = {'startNumber': index, 'endNumber': 30000 + index}
            result = experiment.perform()
            assert result

    report = Scientist.report.get(name)
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 0
    assert str(report)
    assert report.statuses['disabled']
    assert report.statuses['ignored']
    assert report.statuses['match']


def test_default_context():
    # noinspection PyProtectedMember
    name = sys._getframe().f_code.co_name

    Experiment.default_context = {'startNumber': 0}

    for index in range(0, 2000, 100):
        with Scientist(name) as experiment:
            experiment.control.function = lambda **kwargs: SubFib(**kwargs)
            experiment.trial.function = lambda **kwargs: NewSubFib(**kwargs)
            # the lambdas here return generators so we need to tell the experiment to compare generates
            experiment.comparator = experiment.compare_generators
            # context gets combined with default_context
            experiment.context = {'endNumber': 30000 + index}
            result = experiment.perform()
            assert result

    report = Scientist.report.get(name)
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 0
    assert str(report)
    assert report.statuses['match']


def test_context():
    # noinspection PyProtectedMember
    name = sys._getframe().f_code.co_name

    for index in range(0, 2000, 100):
        with Scientist(name) as experiment:
            experiment.control.function = lambda **kwargs: SubFib(**kwargs)
            experiment.trial.function = lambda **kwargs: NewSubFib(**kwargs)
            # the lambdas here return generators so we need to tell the experiment to compare generates
            experiment.comparator = experiment.compare_generators
            # context gets combined with kwargs to perform()
            experiment.context = {'endNumber': 30000 + index}
            result = experiment.perform(startNumber=index)
            assert result

    report = Scientist.report.get(name)
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 0
    assert str(report)
    assert report.statuses['match']


def test_exception():
    # noinspection PyProtectedMember
    name = sys._getframe().f_code.co_name

    for index in range(0, 2000, 100):
        with Scientist(name) as experiment:
            experiment.control.function = lambda **kwargs: SubFib(**kwargs)
            experiment.trial.function = lambda **kwargs: KaboomSubFib(**kwargs)
            # the lambdas here return generators so we need to tell the experiment to compare generates
            experiment.comparator = experiment.compare_generators
            # context gets combined with kwargs to perform()
            experiment.context = {'endNumber': 30000 + index}
            result = experiment.perform(startNumber=index)
            assert result

    report = Scientist.report.get(name)
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results > 0
    assert str(report)
    assert report.statuses['contrite']


def test_before_run():
    # noinspection PyProtectedMember
    name = sys._getframe().f_code.co_name

    def before_run(experiment_):
        experiment_.duty_cycle *= 2

    for index in range(0, 200000, 100):
        with Scientist(name) as experiment:
            experiment.before_run = before_run
            experiment.control.function = lambda **kwargs: SubFib(**kwargs)
            experiment.trial.function = lambda **kwargs: NewSubFib(**kwargs)
            # the lambdas here return generators so we need to tell the experiment to compare generates
            experiment.comparator = experiment.compare_generators
            # for grins, let's only run the trial a quarter of the time and ignore startNumbers on 1000 boundary
            experiment.duty_cycle = 25
            # context gets combined with kwargs to perform()
            experiment.context = {'startNumber': index, 'endNumber': 30000 + index}
            result = experiment.perform()
            assert result

    report = Scientist.report.get(name)
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 0
    assert str(report)
    assert report.statuses['disabled']
    assert report.statuses['match']


