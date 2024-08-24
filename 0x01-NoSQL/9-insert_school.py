#!/usr/bin/env python3
''' inserts a new doc in a collection based on kwargs'''


from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    '''python function to insert a new document in a collection'''
    insert_doc = mongo_collection.insert_one(kwargs)
    return insert_doc.inserted_id
