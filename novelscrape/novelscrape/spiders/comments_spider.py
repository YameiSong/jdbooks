import json
import scrapy
from novelscrape.items import CommentItem
import pymongo
from urllib.parse import urlencode

class CommentsSpider(scrapy.Spider):
    name = "comments"

    base_url = 'https://club.jd.com/comment/skuProductPageComments.action'

    params = {
                'callback': 'fetchJSON_comment98',
                'productId': '0',
                'score': '0',
                'sortType': '5',
                'page': '0',
                'pageSize': '10',
                'isShadowSku': '0',
                'fold': '1'
            }
    
    def start_requests(self):

        # connect to "jdbooks" database
        mongo_uri = self.settings.get('MONGO_URI'),
        mongo_db = self.settings.get('MONGO_DATABASE')
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[mongo_db]

        # get all "product_id" (a list) in the "novels" collection
        product_ids = self.db.novels.find(
            {'product_id': {'$exists': 'true'}}, 
            {'product_id': 1}
            )

        for doc in product_ids:
            pid = doc['product_id']
            self.params.update({'productId': str(pid)})
            url = f'{self.base_url}?{urlencode(self.params)}'

            yield scrapy.Request(
                url=url, 
                callback=self.parse, 
                meta={'product_id': pid, 'page': 0}
                )

    def parse(self, response):
        product_id = response.meta['product_id']
        page = response.meta['page']
        json_str = response.text[20:-2]
        
        if json_str:
            info_dict = json.loads(json_str)
            
            item = CommentItem()
            item['product_id'] = int(product_id)

            comments_list = info_dict['comments']
            for cm in comments_list:
                item['comment_id'] = cm['id']
                item['score'] = cm['score']
                item['content'] = cm['content']
                yield item
            
            if page < info_dict['maxPage'] - 1:
                page += 1
                self.params.update({
                    'productId': str(product_id),
                    'page': str(page)
                    })

                url = f'{self.base_url}?{urlencode(self.params)}'

                yield scrapy.Request(
                    url=url, 
                    callback=self.parse, 
                    meta={'product_id': product_id, 'page': page}
                    )