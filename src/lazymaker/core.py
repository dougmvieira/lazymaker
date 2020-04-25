import json
from collections import namedtuple

from dask.base import tokenize


Cache = namedtuple('Cache', ('value', 'filename'))


def check_dependencies(cache, filename, *args, **kwargs):
    non_cache_args = tuple((arg for arg in args if not isinstance(arg, Cache)))
    input_hash = tokenize((non_cache_args, kwargs))
    cache_hashes = {arg.filename: cache[arg.filename][0]
                    for arg in args if isinstance(arg, Cache)}
    try:
        _, cached_input_hash, cached_cache_hashes = cache[filename]
        is_updated = (input_hash == cached_input_hash
                      ) and (cache_hashes == cached_cache_hashes)
    except KeyError:
        is_updated = False
    return is_updated, input_hash, cache_hashes


def update_dependencies(cache, cache_filename, output_filename, output,
                        input_hash, cache_hashes):
    output_hash = tokenize(output)
    cache[output_filename] = [output_hash, input_hash, cache_hashes]
    with open(cache_filename, 'w') as f:
        json.dump(cache, f, indent=4)


def persist_memoise(cache_filename, read, persist=None):
    try:
        with open(cache_filename) as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = dict()

    if persist is None:
        def persist(output, filename):
            pass

    def closure(filename, compute, *args, **kwargs):
        if compute is None:
            def compute(*args, **kwargs):
                return read(filename)

        is_updated, input_hash, cache_hashes = check_dependencies(
            cache, filename, *args, **kwargs)
        if is_updated:
            output = read(filename)
        else:
            args_vals = (arg.value if isinstance(arg, Cache) else arg
                         for arg in args)
            output = compute(*args_vals, **kwargs)
            persist(output, filename)
            update_dependencies(cache, cache_filename, filename, output,
                                input_hash, cache_hashes)
        return Cache(output, filename)
    return closure
