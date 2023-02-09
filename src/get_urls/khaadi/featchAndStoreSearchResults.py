import requests
import traceback
from bs4 import BeautifulSoup
from utils.helper import url_insert_bulk

def khaadi_url():
    try:
        message = "start getting url for khaadi"
        print(message)

        url = 'https://pk.khaadi.com/media/sitemap_pk.xml'
        page = requests.get(url)
        if page.status_code != 200:
            message = "Error: khaadi " + page.text
            print(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_xmls = [
            element.text for element in sitemap_index.findAll('loc')]
        for sitemap_xml in sitemap_xmls:
            request_sitemap_xml = requests.get(sitemap_xml)

        if request_sitemap_xml.status_code != 200:
            message = "Error: khaadi " + page.text
            print(message)

        sitemap_urls = BeautifulSoup(request_sitemap_xml.content, 'html.parser')
        urls_formed = [
            element.text for element in sitemap_urls.findAll('loc')]
        for url in urls_formed:
            result = {
                "competitor": "khaadi",
                "url": url,
                "scraper_type": "sitemap"
            }
            outputs.append(result)
            if len(outputs) == 5000:
                url_insert_bulk(outputs)
                outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        print(message)

khaadi_url()