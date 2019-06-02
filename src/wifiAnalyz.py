import pymongo
import pprint
import datetime
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@cluster0-qnboi.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

collection = db.test_collection
post = {"author": "Mike",
"text": "My first blog post!",
"tags": ["mongodb", "python", "pymongo"],
"date": datetime.datetime.utcnow()}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
