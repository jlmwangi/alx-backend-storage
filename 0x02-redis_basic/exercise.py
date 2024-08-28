#!/usr/bin/env python3
'''writing strings ro redis'''


import redis
import uuid


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
