import json

from dask.base import tokenize


def check_dependencies(cache, filename, *args, **kwargs):
    input_hash = tokenize((args, kwargs))
    try:
        _, cached_input_hash = cache[filename]
        is_updated = input_hash == cached_input_hash
    except KeyError:
        is_updated = False
    return is_updated, input_hash


def update_dependencies(cache, cache_filename, output_filename, output,
                        input_hash):
    output_hash = tokenize(output)
    cache[output_filename] = [output_hash, input_hash]
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

        is_updated, input_hash = check_dependencies(
            cache, filename, *args, **kwargs)
        if is_updated:
            output = read(filename)
        else:
            output = compute(*args, **kwargs)
            persist(output, filename)
            update_dependencies(cache, cache_filename, filename, output,
                                input_hash)
        return output
    return closure
