import os

from lazymaker import persist_memoise


def test():
    cache_filename = 'cache.json'
    counters = [0, 0]
    mock_persist = dict()

    def evals_count(i):
        counters[i] += 1
        return counters[i]

    def persist(output, filename):
        mock_persist[filename] = output

    try:
        os.remove(cache_filename)
    except FileNotFoundError:
        pass

    memo = persist_memoise(cache_filename, mock_persist.get, persist)

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

    os.remove(cache_filename)
