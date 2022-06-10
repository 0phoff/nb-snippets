#
#   Cache function outputs for faster notebook execution
#   Tanguy Ophoff
#

def cache(*args, basefolder='/tmp', extension='.pkl', save_fn=None, load_fn=None):
    """
    Cache the result of a function to a file.
    By default the saving/loading happens with the pickle module, but you can specify your own funcitons.

    Args:
        *args: Should not be used, this is here so you can omit braces on the decorator if the defaults are ok
        basefolder (str): Folder to store the cache files; Default '/tmp'
        extension (str): File extension (should start with a dot); Default '.pkl'
        save_fn (Callable[[T, Path], None]): Function to save your object; Default pickle.dump
        load_fn (Callable[[Path], T]): Function to load your object; Default pickle.load

    Examples:
        >>> @cache
        ... def foo(value):
        ...     time.sleep(5)
        ...     return value

        # Store cache results in local folder
        >>> @cache(basefolder='.')
        ... def bar(value):
        ...     time.sleep(5)
        ...     return value

        # Custom functions for dataframes (This is basically a reimplementation of cache_df)
        >>> @cache(save_fn=lambda df, path: df.to_pickle(path), load_fn=lambda path: pd.read_pickle(path))
        ... def foo_df(**data):
        ...     time.sleep(5)
        ...     return pd.DataFrame(data)
    """
    import logging
    import pickle
    from functools import wraps
    import hashlib
    from pathlib import Path

    log = logging.getLogger('cache')

    if save_fn is None:
        def save_fn(obj, path):
            with open(path, 'wb') as f:
                pickle.dump(obj, f)

    if load_fn is None:
        def load_fn(path):
            with open(path, 'rb') as f:
                return pickle.load(f)

    def cache_inner(func):
        # Compute function hash
        func_string = (
            func.__code__.co_code + 
            "".join(str(cnst) for cnst in func.__code__.co_consts).encode() + 
            "".join(func.__code__.co_freevars).encode()
        )
        func_hash = hashlib.md5(func_string)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Uppdate hash with args
            total_hash = func_hash.copy()
            total_hash.update((str(args) + str(kwargs)).encode())
            digest = total_hash.hexdigest()
            
            # Get cached path
            cache_path = (Path(basefolder) / f'cache-{digest}').with_suffix(extension)
            
            # Run function if necessary
            if cache_path.exists():
                log.warning(f'Using cache for "{func.__name__}" [{cache_path}]')
                return load_fn(cache_path)
            else:
                obj = func(*args, **kwargs)
                save_fn(obj, cache_path)
                log.info(f'Saved cache for "{func.__name__}" [{cache_path}]')
                return obj

        return wrapper

    if len(args) > 0:
        return cache_inner(args[0])
    return cache_inner


def cache_df(*args, basefolder='/tmp'):
    """
    Wrapper around cache with defaults for pandas DataFrame objects.

    Args:
        *args: Should not be used, this is here so you can omit braces on the decorator if the defaults are ok
        basefolder (str): Folder to store the cache files; Default '/tmp'

    Examples:
        >>> @cache_df
        ... def foo(**data):
        ...     time.sleep(5)
        ...     return pd.DataFrame(data)

        # Store cache results in local folder
        >>> @cache_df(basefolder='.')
        ... def bar(**data):
        ...     time.sleep(5)
        ...     return pd.DataFrame(data)
    """
    import pandas as pd

    return cache(
        *args,
        basefolder=basefolder,
        extension='.pkl',
        save_fn=lambda df, path: df.to_pickle(path),
        load_fn=pd.read_pickle,
    )


if __name__ == '__main__':
    print('functions: cache, cache_df')
