#!/usr/bin/env python3
'''script that provides some stats about nginx logs stored in mongodb'''


from pymongo import MongoClient

'''set up mongodb connection'''
client = MongoClient('mongodb://localhost:27017/')
db = client.logs  # database name
collection = db.nginx  # collection name
no_docs = collection.count_documents({})  # count no of documents

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_counts = {method: 0 for method in methods}  # initialize method counters


print('{} logs'.format(no_docs))

for log in collection.find():  # count occurences of each method
    if log.get("method") in method_counts:
        method_counts[log["method"]] += 1

print('Methods:')  # print method statistics
for method in methods:
    print(f"\tmethod {method}: {method_counts[method]}")

print(f"{collection.status}")
