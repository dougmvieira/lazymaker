import json
import logging
from hashlib import sha1


def make_hashable(obj):
    if isinstance(obj, str):
        return obj.encode('utf-8')
    else:
        return bytes(obj)


def hash_tuple(objs):
    h = sha1()
    for obj in objs:
        if hasattr(obj, 'lazymaker_hash'):
            obj = obj.lazymaker_hash
        h.update(make_hashable(obj))
    return h.hexdigest()


def check_dependencies(cache, filename, args):
    args_hash = hash_tuple(args)
    try:
        cached_args_hash = cache[filename]
        is_updated = args_hash == cached_args_hash
    except KeyError:
        is_updated = False
    return is_updated, args_hash


def update_dependencies(cache, cache_filename, name, args_hash):
    cache[name] = args_hash
    with open(cache_filename, 'w') as f:
        json.dump(cache, f, indent=4)


def lazymake(cache_filename, name, compute, args, read):
    try:
        with open(cache_filename) as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = dict()

    is_updated, args_hash = check_dependencies(cache, name, args)
    is_read = False
    if is_updated:
        try:
            output = read(name)
            is_read = True
        except Exception:
            logging.warning('Could not read {}. Computing instead.'
                            ''.format(name))

    if not is_updated or not is_read:
        output = compute(*args)
        update_dependencies(cache, cache_filename, name, args_hash)

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
