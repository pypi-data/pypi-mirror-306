import inspect
import json
import os
from functools import wraps
from typing import Optional, Callable

import redis
from flask import g
from redis.backoff import NoBackoff
from redis.retry import Retry


class CtRedis:
    """
    CtRedis provides caching functionality with Redis, utilizing a decorator-based caching approach.

    Attributes:
        cache_enabled (bool): A flag indicating if caching is enabled at the service level.
        redis_pool (redis.ConnectionPool): Redis connection pool for managing Redis connections.
        expire_time (int): Default expiration time (in seconds) for cache entries.
        logger (logging.Logger): Logger instance for logging cache activity and exceptions.
    """

    def __init__(self, is_cache_enabled, logger, redis_pool, expire_time=60):
        """
        Initializes the CtRedis instance.

        Args:
            is_cache_enabled (bool): Flag to enable/disable caching.
            logger (logging.Logger): Logger for logging cache-related information.
            redis_pool (redis.ConnectionPool): Connection pool for Redis.
            expire_time (int): Default expiration time for cache entries.
        """
        self.logger = logger
        self.cache_enabled = is_cache_enabled
        self.redis_pool = redis_pool
        self.expire_time = expire_time

    def cache(self, template_cache_key: str, field: str, expire_time: Optional[int] = None,
              is_global: Optional[bool] = False) -> Callable:
        """
        Decorator for caching function results in Redis.

        Args:
            template_cache_key (str): Cache key template with placeholders.
            field (str): Field within the cache key for caching specific values.
            expire_time (Optional[int]): Expiration time for the cache entry.
            is_global (Optional[bool]): Flag indicating if the cache key is global.

        Returns:
            Callable: Wrapped function with caching functionality.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                func_output = None
                use_cache = kwargs.pop('use_cache', True)
                if not self.cache_enabled or not self.redis_pool or not use_cache:
                    return func(*args, **kwargs)
                try:
                    if 'redis_conn' not in g:
                        redis_conn = get_redis_connection(self.redis_pool)
                        pipe = redis_conn.pipeline()
                        pipe.multi()
                        g.pipe = pipe
                        g.redis_conn = redis_conn
                    generated_cache_key, hash_field = self.__generate_cache_key_and_hash_field(template_cache_key, func,
                                                                                               field,
                                                                                               is_global,
                                                                                               *args)
                    hash_value_from_cache = g.redis_conn.hget(generated_cache_key, hash_field)
                    if hash_value_from_cache is not None:
                        return json.loads(hash_value_from_cache)
                    else:
                        func_output = func(*args, **kwargs)
                        g.pipe.hset(generated_cache_key, hash_field, json.dumps(func_output))
                        g.pipe.expire(generated_cache_key,
                                      expire_time if expire_time is not None else self.expire_time)
                        return func_output
                except TypeError as error:
                    self.logger.info("Caught exception from cache  :: {}".format(error))
                    return func_output if func_output is not None else func(*args, **kwargs)
                except Exception as error:
                    self.logger.info("Caught exception from cache  :: {}".format(error))
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def __generate_cache_key_and_hash_field(self, template_cache_key: str, func: Callable, template_hash_field: str,
                                            is_global: bool, *args) -> tuple:
        """
        Generates the cache key and hash field for caching purposes.

        Args:
            template_cache_key (str): The cache key template with placeholders.
            func (Callable): The function being cached.
            template_hash_field (str): Template for the hash field.
            is_global (bool): Indicates if the key should be global.
            args: Arguments passed to the decorated function.

        Returns:
            tuple: Tuple containing the generated cache key and hash field.
        """
        env = os.getenv("ENVIRONMENT").lower()
        # get full args from the function
        arg_values = dict(zip(inspect.getfullargspec(func).args, args))
        cache_key = template_cache_key  # ':$abc.xyz'
        for arg_name, arg_value in arg_values.items():
            placeholder_start = f':${arg_name}.'  # ':$abc.'
            while placeholder_start in cache_key:
                key_start = cache_key.find(placeholder_start) + len(placeholder_start)  # key starting length
                key_end = cache_key.find(':', key_start)  # key ending length
                key_placeholder = cache_key[key_start:key_end] if key_end != -1 else cache_key[
                                                                                     key_start:]  # xyz from $abc.xyz
                if key_placeholder:
                    attr_value = self.__get_nested_attribute_value(arg_value, key_placeholder)  # value of abc.xyz
                    cache_key = cache_key.replace(f'${arg_name}.{key_placeholder}',
                                                  str(attr_value) if attr_value is not None else 'None')
                else:
                    break
            # Replace the cache key name with value if there is not nested attribute
            cache_key = cache_key.replace(f':${arg_name}', f':{arg_value}')

        hash_field = self.__get_nested_attribute_value(arg_values, template_hash_field.split('$', 1)[1]) \
            if '$' in template_hash_field else template_hash_field
        hash_field = str(hash_field) if hash_field is not None else template_hash_field.split('$')[1].split('.')[0]

        env = '' if env == 'prod' else env + ':'
        cache_key = f"{env}{cache_key}" if is_global else \
            f"{env}{self.redis_pool.connection_kwargs.get('client_name')}:{cache_key}"
        return cache_key, str(hash_field)

    @staticmethod
    def __get_nested_attribute_value(obj, attr_path):
        """
        Retrieves the value of a nested attribute from an object or JSON-like dictionary.

        Args:
            obj (Any): The object or dictionary to retrieve the attribute from.
            attr_path (str): Dot-separated path to the nested attribute.

        Returns:
            Any: Value of the nested attribute if found, raises an Exception if not found.

        Raises:
            Exception: If the attribute path is invalid.
        """
        attrs = attr_path.split('.')
        attr_val = obj
        for attr in attrs:
            if hasattr(attr_val, attr):
                attr_val = getattr(attr_val, attr)
            elif isinstance(attr_val, dict) and attr in attr_val:
                attr_val = attr_val[attr]
            else:
                raise Exception(attr + ' not found in the hash_field or cache_key')
        return attr_val


def get_redis_connection(redis_pool, retries: int = 2):
    return redis.Redis(connection_pool=redis_pool, retry_on_timeout=True,
                       retry=Retry(retries=retries, backoff=NoBackoff(),
                                   supported_errors=(ConnectionError, TimeoutError)))


def configure_redis_pool(host: str, port: int, client_name: str, max_connections: int = 30,
                         cache_enabled: bool = False):
    redis_pool = None
    if cache_enabled and host and port:
        try:
            env = os.getenv("ENVIRONMENT").lower()
            redis_pool = redis.ConnectionPool(host=host,
                                              port=port,
                                              client_name=client_name,
                                              max_connections=max_connections
                                              )
            redis_conn = get_redis_connection(redis_pool)

            delete_pattern = f"{env}:{client_name}:*"
            with redis_conn.pipeline() as pipe:
                for key in redis_conn.scan_iter(delete_pattern):
                    pipe.delete(key)
                pipe.execute()

            return redis_pool
        except Exception:
            return None
    else:
        return redis_pool
