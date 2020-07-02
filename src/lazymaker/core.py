import json
from functools import reduce
from hashlib import sha1


def make_hashable(obj):
    if isinstance(obj, str):
        return obj.encode('utf-8')
    else:
        return bytes(obj)


def hash_singleton(obj):
    return sha1(make_hashable(obj)).hexdigest()


def hash_tuple(objs):
    h = sha1()
    reduce(lambda _, x: h.update(x), map(make_hashable, objs))
    return h.hexdigest()


def check_dependencies(cache, filename, *args):
    input_hash = hash_tuple(args)
    try:
        _, cached_input_hash = cache[filename]
        is_updated = input_hash == cached_input_hash
    except KeyError:
        is_updated = False
    return is_updated, input_hash


def update_dependencies(cache, cache_filename, output_filename, output,
                        input_hash):
    output_hash = hash_singleton(output)
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

    def closure(filename, compute, *args):
        if compute is None:
            def compute(*args):
                return read(filename)

        is_updated, input_hash = check_dependencies(
            cache, filename, *args)
        if is_updated:
            output = read(filename)
        else:
            output = compute(*args)
            persist(output, filename)
            update_dependencies(cache, cache_filename, filename, output,
                                input_hash)
        return output
    return closure
