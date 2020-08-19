# To force scrapy to output string instead of unicode in JSON file,
# add the following line in settings.py:
# FEED_EXPORT_ENCODING = 'utf-8'

# use the following cmd to output to JSON:
# output to a json file by using scrapy Feed Exports:
# scrapy crawl novels -o novels.json

# output to mongodb:
# scrapy crawl novels

import scrapy
from novelscrape.items import NovelscrapeItem

class NovelsSpider(scrapy.Spider):
    name = "novels"
    start_urls = [
        'https://channel.jd.com/1713-3258.html'
    ]

    def parse(self, response):
        for novel in response.css('.mc .p-name').xpath('.//a'):
            item = NovelscrapeItem()
            item['title'] = novel.css('::text').get()
            item['detail_page'] = novel.attrib['href']
            yield item