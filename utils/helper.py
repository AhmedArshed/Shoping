import traceback
from time import sleep
from pymongo import UpdateOne

from dateutil.relativedelta import relativedelta
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from requests.adapters import HTTPAdapter
from config.index import DB_NAME
from services.mongo_db.connection import client

db = client[DB_NAME]


def url_insert(item):
    try:
        print("inside url_insert mongo")
        if type(item) is not dict:
            return
        filter = {
            "competitor": item["competitor"],
            "url": item["url"],
            "scraper_type": item["scraper_type"]
        }
        db.competitor_url.update_one(filter, {"$setOnInsert": item}, True)
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        print(message)


def url_insert_bulk(data):
    try:
        print("inside url_insert_bulk mongo")
        if type(data) is not list or len(data) == 0:
            return
        rows = []
        for item in data:
            filter = {
                "competitor": item["competitor"],
                "url": item["url"],
                "scraper_type": item["scraper_type"]
            }
            rows.append(UpdateOne(filter, {"$setOnInsert": item}, True))
        db.competitor_url.bulk_write(rows)
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        print(message)

