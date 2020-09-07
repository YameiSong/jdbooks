import json
import scrapy
from novelscrape.items import CommentItem
import pymongo

class CommentsSpider(scrapy.Spider):
    name = "comments"

    base_url = 'https://club.jd.com/comment/skuProductPageComments.action'

    def __init__(self):
        # connect to "jdbooks" database
        mongo_uri = self.settings.get('MONGO_URI'),
        mongo_db = self.settings.get('MONGO_DATABASE')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        # create a collection "comments"
        self.comments = self.db['comments']

        # get all "product_id" (a list) in the "novels" collection
        self.product_ids = self.db.novels.find({}, {'product_id': 1, '_id': 0})
    
    def start_requests(self):

        for pid in self.product_ids:
            params = {
                'callback': 'fetchJSON_comment98',
                'productId': pid,
                'score': 0,
                'sortType': 5,
                'page': 0,
                'pageSize': 10,
                'isShadowSku': 0,
                'fold': 1
            }

            yield scrapy.FormRequest(
                url=self.base_url, 
                formdata=params, 
                callback=self.parse, 
                meta={'product_id': pid, 'page': 0}
                )

    def parse(self, response):
        product_id = response.meta['product_id']
        page = response.meta['page']

        json_str = response.text[20:-2]
        info_dict = json.loads(json_str)
        
        item = CommentItem()
        item['product_id'] = product_id

        comments_list = info_dict['comments']
        for cm in comments_list:
            item['score'] = cm['score']
            item['content'] = cm['content']
            yield item
        
        if page < info_dict['maxPage'] - 1:
            page += 1

            params = {
                'callback': 'fetchJSON_comment98',
                'productId': product_id,
                'score': 0,
                'sortType': 5,
                'page': page,
                'pageSize': 10,
                'isShadowSku': 0,
                'fold': 1
            }

            yield scrapy.FormRequest(
                url=self.base_url, 
                formdata=params, 
                callback=self.parse, 
                meta={'product_id': product_id, 'page': page}
                )
        else:
            return