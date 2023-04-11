
import os
import pymongo
from pymongo import MongoClient, InsertOne
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread
from config.index import DB_NAME
from services.mongo_db.connection import client

db = client[DB_NAME]


def extract_url(name):
    try:
        skip = 0
        chunk = 50000
        urls_count = True
        urls = []
        print(
            f"Getting {name}'s product urls ")
        while urls_count:
            cursor = db.competitor_url.find(
                {"competitor": name}, {"url": 1, "_id": 0}).skip(skip).limit(chunk)
            local_urls = [item['url'] for item in cursor]
            urls.extend(local_urls)
            urls_count = len(local_urls)
            skip += chunk
        return urls
    except Exception as e:
        print(e)
