from threading import Thread
from flask import Flask, Response, request

from routes.crawl.index import crawl_routes
from routes.get_url.index import url_routes

app = Flask(__name__)

app.register_blueprint(crawl_routes,url_prefix="")
app.register_blueprint(url_routes,url_prefix="")


if __name__ == "__main__":
    app.run(port=5102)