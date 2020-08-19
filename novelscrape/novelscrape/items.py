# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    detail_page = scrapy.Field()

class DetailItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    star = scrapy.Field()

class CommentItem(scrapy.Item):
    title = scrapy.Field()
    star = scrapy.Field()
    comment = scrapy.Field()