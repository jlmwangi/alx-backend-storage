#!/usr/bin/env python3
'''changes all topics of a school doc based on the name'''


from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    '''updates topics of a school based on the name'''
    update_topic = mongo_collection.update_one(
            { "name": name },
            { $set: { "topics": topics } }
    )
    return update_topic
