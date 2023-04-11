import scrapy
import pydash
import traceback
from datetime import datetime, date
from dateutil.parser import parse
from user_agent import generate_user_agent, generate_navigator
from scraper.scraper.get_urls import extract_url

class KhaadiQuotesSpider(scrapy.Spider):
    name = "khaadi"
    custom_settings = {
        'USER_AGENT': generate_user_agent(),
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        },
        'CONCURRENT_ITEMS': 50,
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_IP': 20,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 16
    }

    def __init__(self, urls):
        urls = extract_url(self.name)
            

    def parse(self, response):
        try:  
            product_name = response.xpath('//h1[@class="product-name"]/text()').get()
            price = response.xpath('//span[@class="price"]/text()').get()
            description = response.xpath('//div[@class="product-description"]//p/text()').get()
            image_url = response.xpath('//img[@class="active"]/@src').get()
            yield {
                'Product Name': product_name,
                'Price': price,
                'Description': description,
                'Image URL': image_url
            }
        except Exception as e:
            message = "Error: " + str(e) + "\n" + traceback.format_exc()
            print(message)
