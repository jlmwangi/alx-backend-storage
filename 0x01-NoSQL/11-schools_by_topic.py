#!/usr/bin/env python3
'''returns list of school having a specific topic'''


from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    '''topic string to be searched'''
    school_list = list(mongo_collection.find({ "topic": topic }))
    return school_list
