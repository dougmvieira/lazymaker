import json
import logging
from functools import reduce
from hashlib import sha1


def make_hashable(obj):
    if isinstance(obj, str):
        return obj.encode('utf-8')
    else:
        return bytes(obj)


def hash_singleton(obj):
    if hasattr(obj, 'lazymaker_hash'):
        obj = obj.lazymaker_hash
    return sha1(make_hashable(obj)).hexdigest()


def hash_tuple(objs):
    h = sha1()
    for obj in objs:
        if hasattr(obj, 'lazymaker_hash'):
            obj = obj.lazymaker_hash
        h.update(make_hashable(obj))
    return h.hexdigest()


def check_dependencies(cache, filename, args):
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


def persist_memoise(cache_filename, compute, args, read, address):
    try:
        with open(cache_filename) as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = dict()

    is_updated, input_hash = check_dependencies(cache, address, args)
    is_read = False
    if is_updated:
        try:
            output = read(address)
            is_read = True
        except:
            logging.warning(f'Could not read {address}. Computing instead.')

    if not is_updated or not is_read:
        output = compute(*args)
        update_dependencies(cache, cache_filename, address, output,
                            input_hash)

    return output


def add_side_effects(compute, side_effects):
    def closure(*args, **kwargs):
        output = compute(*args, **kwargs)
        side_effects(output)
        return output

    return closure


def add_dummy_args(compute, n):
    def closure(*args):
        return compute(*args[:-n])
    return closure
