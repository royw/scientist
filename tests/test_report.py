# coding=utf-8

"""
Using 2 different algorithms for calculating fibonacci sequence (from
http://stackoverflow.com/questions/494594/how-to-write-the-fibonacci-sequence-in-python)
as control and trial experiment.
"""
from scientist.in_memory_report import InMemoryReport
from scientist.report import Report
from scientist.science import Science
from math import sqrt

__docformat__ = 'restructuredtext en'

Science.report = InMemoryReport


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


def test_summary():
    def original(**kwargs):
        return list(SubFib(**kwargs))

    def trial(**kwargs):
        return list(NewSubFib(**kwargs))

    for index in range(0, 2000, 100):
        with Science('Fibonacci subsets') as experiment:
            experiment.control_function = original
            experiment.trial_function = trial
            result = experiment.perform(startNumber=index, endNumber=3000 + index)
            assert result

    report = Science.report.get('Fibonacci subsets')
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 0
    assert str(report)


def test_summary_with_bug():
    def original(**kwargs):
        return list(SubFib(**kwargs))

    def trial(**kwargs):
        return list(BuggySubFib(**kwargs))

    for index in range(0, 2000, 100):
        with Science('Fibonacci subsets') as experiment:
            experiment.control_function = original
            experiment.trial_function = trial
            experiment.perform(startNumber=index, endNumber=3000 + index)

    report = Science.report.get('Fibonacci subsets')
    report.summarize()
    print(str(report))
    assert report.control_count > 0
    assert report.enabled_count > 0
    assert report.contrary_results == 1
    assert str(report)
