# To force scrapy to output string instead of unicode in JSON file,
# add the following line in settings.py:
# FEED_EXPORT_ENCODING = 'utf-8'

# use the following cmd to output to JSON:
# output to a json file by using scrapy Feed Exports:
# scrapy crawl novels -o novels.json

# output to mongodb:
# scrapy crawl novels

import json
import scrapy
from novelscrape.items import NovelscrapeItem
from scrapy.utils.response import open_in_browser

class NovelsSpider(scrapy.Spider):
    # debug: i is an assistant for debugging
    i = 0

    name = "novels"
    start_urls = [
        'https://channel.jd.com/1713-3258.html'
    ]

    def __init__(self):
        with open('cookies.json', 'r') as f:
            self.cookies = json.load(f)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        for novel in response.css('.mc .p-name').xpath('.//a'):
            item = NovelscrapeItem()
            item['title'] = novel.css('::text').get()
            item['detail_page'] = novel.attrib['href']
            detail_page_url = response.urljoin(item['detail_page'])
            request = scrapy.Request(
                detail_page_url, 
                callback=self.parse_details,
                cb_kwargs=dict(item = item),
                cookies=self.cookies,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
                )
            yield request
    
    def parse_details(self, response, item):
        # debug: view the response in browser
        if self.i == 0:
            open_in_browser(response)
            self.i += 1

        # log the url of detail page
        # self.logger.info('Parse function called on %s', response.url)

        item['author'] = response.css('.p-author a::text').get()
        # 价格是用js动态渲染的，要换方法抓取
        item['price'] = response.css('.p-price::text').get()
        yield item


# import scrapy
# from novelscrape.items import DetailItem
# import pymongo

# class NovelDetailsSpider(scrapy.Spider):
#     name = "details"

#     def __init__(self):
#         # connect to "jdbooks" database
#         mongo_uri = self.settings.get('MONGO_URI'),
#         mongo_db = self.settings.get('MONGO_DATABASE', 'items')
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#         # get a cursor that points to all "detail_page" in the "novels" collection
#         self.detail_page_urls = self.db.novels.find({}, {detail_page: 1, _id: 0})

#     def parse(self, response):
#         for doc in self.detail_page_urls:
#             url = doc['detail_page']
            