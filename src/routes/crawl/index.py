import os
import traceback
import crochet
import logging
from flask import Blueprint, Response, request
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from src.utils.helper import *
from src.scraper.scraper.mappings import SCRAPPERS

crawl_routes = Blueprint("crawl_routes", __name__)

CRAWL_STATUS = "initial"
crawler = CrawlerRunner(get_project_settings())
try:
    crochet.setup()
except Exception as e:
    message = "Error: " + str(e) + "\n" + traceback.format_exc()
    print(message)

logging.basicConfig(
    filename='scrappy-logs.txt',
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

settings_file_path = 'src.compitator_scraper.compitator_scraper.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)



@crochet.run_in_reactor
def scrape_with_crochet(update_id, competitors, urls):
    try:
        logger.info("Scrape with crochet")
        for name in competitors:
            spider = SCRAPPERS.get(name, None)
            if spider is not None:
                logger.info("Scrape with crochet ")
                logger.info(spider)
                _urls = urls.get(name, []) if type(urls) is dict else urls
                logger.info("adding crawler ")
                logger.info(name)
                should_run = True
                crawler.crawl(spider, urls=_urls)
        if should_run:
            logger.info("setting crawler status")
            deferred = crawler.join()
            logger.info("result after joing crawler ")
            logger.info(deferred)
            deferred.addBoth(lambda _: stop_spiders_crawler(update_id))
            logger.info("Runing Crawler...")
        else:
            print("Exiting Spiders Crawler...")
            update_logs(update_id)
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        print(message)
        return Response("{'message': '"+str(e)+"'}", status=500, mimetype='application/json')


@crawl_routes.route('/crawl', methods=['POST'])
def crawl_for_quotes():
    try:
        if not request.is_json:
            return 'Missing JSON in request', 400
        logger.info("After setting proxy")
        data = request.get_json()
        competitors = data.get('competitors', SCRAPPERS.keys())
        products = data.get('products', [])
        is_match = data.get('isMatched')
        retry_non_scraped_url = data.get('retry', None)

        if type(competitors) is not list or type(products) is not list:
            return Response("{'message': 'Incorrect parameters type!'}", status=400, mimetype='application/json')
        competitors = SCRAPPERS.keys() if len(competitors) == 0 else competitors
        logger.info(competitors)
        update_id = data.get('id')

        urls = {} if len(products) > 0 else []
        print("Getting URls for all competitors")
        for competitor in competitors:
            if len(products) > 0:
                _urls = get_competitor_urls(competitor, products)
                urls[competitor] = _urls
        scrape_with_crochet(update_id, competitors, urls)
        print("{'message': 'Started crawling...'}")
        return Response("{'message': 'Started crawling...'}", status=200, mimetype='application/json')
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        print(message)
        return Response("{'message': '"+str(e)+"'}", status=500, mimetype='application/json')

def stop_spiders_crawler(update_id):
    print("Stopping and exiting Spiders Crawler...")
    update_logs(update_id)