#!/usr/bin/env python3
'''list all documents in a collection'''

from pymongo import MongoClient


def list_all(mongo_collection):
    '''function t list all the docs'''
    if mongo_collection is not None:
        '''if collection object has documents'''
        docs = mongo_collection.find()
        all_docs = list(docs)
        return all_docs
    else:
        return []

#if __name__ == "__main__":
#    list_all
