#!/usr/bin/env python3
'''writing strings ro redis'''


import redis
import uuid
from typing import Callable, Optional, Union


class Cache:
    '''contains two methods, an init method to store a private redis instance
    and a store method to store input data using the random key generated'''
    def __init__(self):
        '''an instance of redis'''
        self._redis = redis.Redis()
        self._redis.flushdb()  # flush the current database

    def store(self, data: str | bytes | int | float) -> str:
        '''generates a random key and stores input data in redis
        using the key'''
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable[bytes], Union[str,
            bytes, int, float]] = None) -> Optional[Union[str,
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
