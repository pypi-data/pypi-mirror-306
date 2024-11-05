'''
Based on https://github.com/iamsinghrajat/async-cache/tree/master
'''
import asyncio
import typing as tp
from collections import OrderedDict
import msgspec
import datetime
from functools import wraps


class LRU:
    '''
    Cache decorator for functions.
    Supports mutable arguments like lists. Still tries to hash them.
    '''
    def __init__(self, maxsize=None, class_method=False, logger=None):
        """
        :param maxsize: Use maxsize as None for unlimited size cache
        :param class_method: Set True to ignore the first "self" argument
        :param logger: if set, this function will print debug logs when cache is used
        """
        self.lru = _LRU(maxsize=maxsize)
        self.class_method = class_method
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, use_cache=True, **kwargs):
            if use_cache:
                # Make key for caching
                key_args = args[1:] if self.class_method else args
                key = _KEY(key_args, kwargs)
                # Call function or use cached value
                if key not in self.lru:
                    self.lru[key] = func(*args, **kwargs)
                else:
                    if self.logger is not None:
                        self.logger.debug(f'Using cached {key_args} {kwargs}')
                return self.lru[key]
            else:
                return func(*args, **kwargs)

        wrapper.__name__ += func.__name__

        return wrapper


class AsyncLRU:
    '''
    Cache decorator for async functions.
    Supports mutable arguments like lists. Still tries to hash them.

    Difference from https://github.com/iamsinghrajat/async-cache/tree/master:
    * If function is not computed yet, but called second time, it waits instead of starting a new coroutine
    * Can be class method and use logger
    '''
    def __init__(self, maxsize=None, class_method=False, logger=None):
        """
        :param maxsize: Use maxsize as None for unlimited size cache
        :param class_method: Set True to ignore the first "self" argument
        :param logger: if set, this function will print debug logs when cache is used
        """
        self.lru = _LRU(maxsize=maxsize)
        self.class_method = class_method
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, use_cache=True, **kwargs):
            if use_cache:
                # Make key for caching
                key_args = args[1:] if self.class_method else args
                key = _KEY(key_args, kwargs)
                # Call function or use cached value
                if key not in self.lru:
                    self.lru[key] = asyncio.create_task(func(*args, **kwargs))
                else:
                    if self.logger is not None:
                        self.logger.debug(f'Using cached {key_args} {kwargs}')
                return await self.lru[key]
            else:
                return await func(*args, **kwargs)

        wrapper.__name__ += func.__name__

        return wrapper


class RedisAsyncCache:
    """
    Cache decorator for async functions.
    Supports mutable arguments like lists. Still tries to hash them.

    Warning: This Redis variant of cacher is only for async functions whose output can be converted to json.
    """
    def __init__(self, name, expire: datetime.timedelta | None = None, class_method=False, logger=None):
        """
        :param name: Name of function, for cache prefix
        :param expire: Expiration time
        :param class_method: Set True to ignore the first "self" argument
        :param logger: if set, this function will print debug logs when cache is used
        """
        self.name = name
        self.class_method = class_method
        self.expire = expire
        import redis
        self.redis = redis.asyncio.Redis()
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, use_cache=True, **kwargs):
            if use_cache:
                # Make key for caching
                key_args = args[1:] if self.class_method else args
                key = self.name + ' -- ' + str(_KEY(key_args, kwargs))
                # Call function or use cached value
                value_enc = await self.redis.get(key)
                if value_enc is None:
                    value = await func(*args, **kwargs)
                    value_enc = msgspec.json.encode(value)
                    await self.redis.set(key, value_enc, ex=self.expire)
                else:
                    value = msgspec.json.decode(value_enc)
                    if self.logger is not None:
                        self.logger.debug(f'Using cached {self.name} {key_args} {kwargs}')
                return value
            else:
                return await func(*args, **kwargs)

        wrapper.__name__ += func.__name__

        return wrapper


class RedisCache:
    """
    Cache decorator for functions.
    Supports mutable arguments like lists. Still tries to hash them.

    Warning: This Redis variant of cacher is only for functions whose output can be converted to json.
    """
    def __init__(self, name, expire: datetime.timedelta | None = None, class_method=False, logger=None):
        """
        :param name: Name of function, for cache prefix
        :param expire: Expiration time
        :param class_method: Set True to ignore the first "self" argument
        :param logger: if set, this function will print debug logs when cache is used
        """
        self.name = name
        self.class_method = class_method
        self.expire = expire
        import redis
        self.redis = redis.Redis()
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, use_cache=True, **kwargs):
            if use_cache:
                # Make key for caching
                key_args = args[1:] if self.class_method else args
                key = self.name + ' -- ' + str(_KEY(key_args, kwargs))
                # Call function or use cached value
                value_enc = self.redis.get(key)
                if value_enc is None:
                    value = func(*args, **kwargs)
                    value_enc = msgspec.json.encode(value)
                    self.redis.set(key, value_enc, ex=self.expire)
                else:
                    value = msgspec.json.decode(value_enc)
                    if self.logger is not None:
                        self.logger.debug(f'Using cached {self.name} {key_args} {kwargs}')
                return value
            else:
                return func(*args, **kwargs)

        wrapper.__name__ += func.__name__

        return wrapper


class _LRU(OrderedDict):
    def __init__(self, maxsize, *args, **kwargs):
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.maxsize and len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]


class _KEY:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        kwargs.pop("use_cache", None)

    def __eq__(self, obj):
        return hash(self) == hash(obj)

    def _get_immutable(self):
        def _hash(param: tp.Any):
            if isinstance(param, tuple):
                return tuple(map(_hash, param))
            if isinstance(param, dict):
                return tuple(map(_hash, param.items()))
            elif hasattr(param, "__dict__"):
                return str(vars(param))
            else:
                return str(param)

        return _hash(self.args) + _hash(self.kwargs)

    def __str__(self) -> str:
        return str(self._get_immutable())

    def __hash__(self):
        return hash(self._get_immutable())
