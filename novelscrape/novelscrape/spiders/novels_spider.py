# To force scrapy to output string instead of unicode in JSON file,
# add the following line in settings.py:
# FEED_EXPORT_ENCODING = 'utf-8'

# use the following cmd to output to JSON:
# output to a json file by using scrapy Feed Exports:
# scrapy crawl novels -o novels.json

# start a splash instance:
# docker run -p 8050:8050 scrapinghub/splash

# output to mongodb:
# scrapy crawl novels

import json
import re

import scrapy
from novelscrape.items import NovelscrapeItem
from scrapy.utils.response import open_in_browser
from scrapy_splash import SplashRequest

from novelscrape.items import CommentItem
import pymongo

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

class NovelsSpider(scrapy.Spider):
    # debug: i is an assistant for debugging
    # i = 0

    name = "novels"
    start_urls = [
        'https://channel.jd.com/1713-3258.html'
    ]

    def __init__(self):
        with open('novelscrape/cookies.json', 'r') as f:
            self.cookies = json.load(f)

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.FormRequest(url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        for novel in response.css('.mc .p-name').xpath('.//a'):
            item = NovelscrapeItem()
            item['title'] = novel.css('::text').get()
            item['detail_page'] = novel.attrib['href']
            detail_page_url = response.urljoin(item['detail_page'])

            request = SplashRequest(
                detail_page_url, 
                self.parse_details,
                meta=dict(item = item),
                cookies=self.cookies,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
                )
            yield request
    
    def parse_details(self, response):
        # debug: view the response in browser
        # if self.i == 0:
        #     open_in_browser(response)
        #     self.i += 1

        # log the url of detail page
        # self.logger.info('Parse function called on %s', response.url)

        item = response.meta['item']
        author = response.css('.p-author a::text').get()
        price = response.css('.dd .p-price::text').get()

        if author: item['author'] = author
        if price: item['price'] = price
        
        yield item


class CommentsSpider(scrapy.Spider):
    name = "comments"

    start_urls = []

    url_id_dict = {}

    def __init__(self):
        # connect to "jdbooks" database
        mongo_uri = self.settings.get('MONGO_URI'),
        mongo_db = self.settings.get('MONGO_DATABASE')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        # get a cursor that points to all "detail_page" and "_id" in the "novels" collection
        self.detail_page_urls = self.db.novels.find({}, {'detail_page': 1})

        for doc in self.detail_page_urls:
            novel_id = doc['_id']
            detail_page = doc['detail_page']
            self.url_id_dict[detail_page] = novel_id

            # Comment JSON example:
            # https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98&productId=12767148&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
            # Note that "skuProductPageComments" means "only shows comments of the current product"; if "productPageComments", shows all relevant books of the same series.
            # Parameters to be modified: 
            #    1) productId: can be extracted from "detail_page" url 
            #    2) page: add 1 to read the next comment page. The JSON file contains "maxPage", so max(page) = maxPage - 1
            # The comment list starts from the word: "comments" in the JSON file

            # generate the first comment link for each product (page = 0)
            x = re.search(r'//item.jd.com/(/d+).html', detail_page)
            product_id = x.group(0)
            first_comment_url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98&productId=' + product_id + '&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            self.start_urls.append(first_comment_url)

    def parse(self, response):
        j = json.loads(response.text)
        item = CommentItem()
        item['novel_id'] = self.url_id_dict[response.request.url] # need to inspect the url

        # to do: extract stars, comments