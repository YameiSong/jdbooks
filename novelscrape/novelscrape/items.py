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
    author = scrapy.Field()
    price = scrapy.Field()
    product_id = scrapy.Field()

class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    product_id = scrapy.Field()
    score = scrapy.Field()
    content = scrapy.Field()