import os
import traceback
import crochet
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from flask import Blueprint, Response, request
from concurrent.futures import ThreadPoolExecutor
from src.scraper.scraper.mappings import SCRAPPERS
from src.get_urls.khaadi.featchAndStoreSearchResults import khaadi_url

crawler = CrawlerRunner(get_project_settings())
try:
    crochet.setup()
except Exception as e:
    message = "Error: " + str(e) + "\n" + traceback.format_exc()
    print(message)

url_routes = Blueprint("url_routes", __name__)

settings_file_path = 'src.scraper.scraper.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

URLS_STATUS = "initial"
SCRAPPING_URLS = False
FUTURES = []


def get_all_urls(competitors):
    try:
        global FUTURES
        executor = ThreadPoolExecutor(len(competitors))
        if 'khaadi' in competitors:
            future = executor.submit(khaadi_url)
            FUTURES.append(future)

    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        print(message)


@url_routes.route("/get-urls", methods=["POST"])
def get_urls():
    try:
        if not request.is_json:
            print('Missing JSON in request 400')
            return 'Missing JSON in request', 400
        data = request.get_json()
        competitors = data.get('competitors', SCRAPPERS.keys())
        if type(competitors) is not list:
            return Response("{'message': 'Incorrect parameters type!'}", status=400, mimetype='application/json')
        competitors = SCRAPPERS.keys() if len(competitors) == 0 else competitors
        global thread
        get_all_urls(competitors)
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        print(message)
        return Response("{'message': '"+str(e)+"'}", status=500, mimetype='application/json')
