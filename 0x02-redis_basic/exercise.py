#!/usr/bin/env python3
'''writing strings ro redis'''


import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps


call_counts = {}


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(*args, **kwargs):
        '''get qualified name of method'''
        method_name = method.__qualname__

        if method_name in call_counts:
            call_counts[method_name] += 1
        else:
            call_counts[method_name] = 1

        return method(*args, **kwargs)  # call original method, return result
    return wrapper


def call_history(method: Callable) -> Callable:
    '''stores history of inputs and outputs'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''generate redis keys for inputs and outputs'''
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'

        self._redis.rpush(input_key, str(args))  # store input args as string

        res = method(self, *args, **kwargs)  # call original method

        self._redis.rpush(output_key, str(res))

        return res
    return wrapper


def replay(method: Callable):
    '''Display history of calls for a particular function.'''
    r = redis.Redis()

    method_name = method.__qualname__
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    ''' Fetch inputs and outputs from Redis'''
    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)

    ''' Display the history'''
    print(f"{method_name} was called {len(inputs)} times:")

    for input_data, output_data in zip(inputs, outputs):
        print(f"{method_name}(*{input_data.decode('utf-8')}) ->
                {output_data.decode('utf-8')}")


class Cache:
    '''contains two methods, an init method to store a private redis instance
    and a store method to store input data using the random key generated'''
    def __init__(self):
        '''an instance of redis'''
        self._redis = redis.Redis()
        self._redis.flushdb()  # flush the current database

    @count_calls
    @call_history
    def store(self, data: str | bytes | int | float) -> str:
        '''generates a random key and stores input data in redis
        using the key'''
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str,
            bytes, int, float]]] = None) -> Optional[Union[str,
                                                     bytes, int, float]]:
        '''optional callable that converts data back to desired format'''
        data = self._redis.get(key)  # get data based on the key
        if data is not None:
            if fn is not None:  # if a callable is provided
                return fn(data)  # transform the data with it
            return data.decode('utf-8')
        return None

    def get_str(self, key: str) -> Optional[str]:
        '''automatically parameterizes Cache.get
        with correct conversion function'''
        return self.get(key, str)

    def get_int(self, key: str) -> Optional[int]:
        ''' automatically parameterizes Cache.get
        with correct conversion function'''
        return self.get(key, lambda x: int(x.decode('utf-8')))
