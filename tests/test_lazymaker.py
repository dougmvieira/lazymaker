import os
from collections import namedtuple

from lazymaker import lazymake, add_side_effects, add_dummy_args


def test():
    cache_filename = 'cache.json'
    counters = [0, 0]
    mock_persist = dict()

    def evals_count(i):
        counters[i] += 1
        return counters[i]

    def persist(output, name):
        mock_persist[name] = output

    try:
        os.remove(cache_filename)
    except FileNotFoundError:
        pass

    def memo(name, compute, *args):
        compute = add_side_effects(compute, lambda o: persist(o, name))
        return lazymake(cache_filename, name, compute, args,
                        mock_persist.__getitem__)

    counter0 = evals_count(0)
    assert counter0 == counters[0] == 1

    counter0 = memo('counter0', evals_count, 0)
    assert counter0 == counters[0] == 2

    counter0 = memo('counter0', evals_count, 0)
    assert counter0 == counters[0] == 2

    counter1 = memo('counter1', evals_count, 1)
    assert counter0 == counters[0] == 2
    assert counter1 == counters[1] == 1

    counter1 = memo('counter1', evals_count, 1)
    assert counter0 == counters[0] == 2
    assert counter1 == counters[1] == 1

    sum_counters = memo('sum', int.__add__, counter0, counter1)
    assert counter0 == counters[0] == 2
    assert counter1 == counters[1] == 1
    assert sum_counters == sum(counters)

    del mock_persist['counter0']
    counter0 = memo('counter0', evals_count, 0)
    assert counter0 == counters[0] == 3

    os.remove(cache_filename)


def test_dummy():
    cache_filename = 'cache.json'
    counter = [0]
    mock_persist = dict()

    def evals_count():
        counter[0] += 1
        return counter[0]

    def persist(output, name):
        mock_persist[name] = output

    try:
        os.remove(cache_filename)
    except FileNotFoundError:
        pass

    def memo(name, compute, *args):
        compute = add_side_effects(compute, lambda o: persist(o, name))
        compute = add_dummy_args(compute, 1)
        return lazymake(cache_filename, name, compute, args,
                        mock_persist.__getitem__)

    memoed = memo('counter', evals_count, 'foo')
    assert memoed == counter[0] == 1

    memoed = memo('counter', evals_count, 'foo')
    assert memoed == counter[0] == 1

    memoed = memo('counter', evals_count, 'bar')
    assert memoed == counter[0] == 2

    os.remove(cache_filename)


def test_custom_lazymaker_hash():
    cache_filename = 'cache.json'
    counter = [0]
    mock_persist = dict()

    CustomType = namedtuple('CustomType', ('count', 'lazymaker_hash',))

    def evals_count():
        counter[0] += 1
        return CustomType(counter[0], counter[0])

    def persist(output, name):
        mock_persist[name] = output

    try:
        os.remove(cache_filename)
    except FileNotFoundError:
        pass

    def memo(name, compute, *args):
        compute = add_side_effects(compute, lambda o: persist(o, name))
        compute = add_dummy_args(compute, 1)
        return lazymake(cache_filename, name, compute, args,
                        mock_persist.__getitem__)

    memoed = memo('counter', evals_count, CustomType('foo', 123))
    assert memoed.count == counter[0] == 1

    memoed = memo('counter', evals_count, CustomType('bar', 123))
    assert memoed.count == counter[0] == 1

    memoed = memo('counter', evals_count, CustomType('foo', 456))
    assert memoed.count == counter[0] == 2

    os.remove(cache_filename)
