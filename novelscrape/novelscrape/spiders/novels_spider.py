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
from scrapy_splash import SplashRequest
# debug:
# from scrapy.utils.response import open_in_browser


class NovelsSpider(scrapy.Spider):
    # debug: i is an assistant for debugging
    # i = 0

    name = "novels"
    start_urls = [
        'https://channel.jd.com/1713-3258.html',
        'https://channel.jd.com/1713-3259.html',
        'https://channel.jd.com/1713-3261.html',
        'https://channel.jd.com/1713-3260.html'
    ]

    def __init__(self):
        with open('novelscrape/cookies.json', 'r') as f:
            self.cookies = json.load(f)

    def parse(self, response):
        for novel in response.css('.mc .p-name').xpath('.//a'):
            item = NovelscrapeItem()
            item['title'] = novel.css('::text').get()
            item['detail_page'] = novel.attrib['href']
            detail_page_url = response.urljoin(item['detail_page'])
            x = re.search(r'item.jd.com\/(\d+).html', item['detail_page'])
            item['product_id'] = int(x.group(1))

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
        if price: item['price'] = float(price)
        
        yield item
