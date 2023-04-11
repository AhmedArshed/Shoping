import pymongo
from pymongo import MongoClient, InsertOne
from config.index import DB_URL

client = pymongo.MongoClient(DB_URL, serverSelectionTimeoutMS=5000)

