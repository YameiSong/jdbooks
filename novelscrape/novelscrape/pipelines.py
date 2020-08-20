# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
# To query document by _id, I must convert id from string to ObjectId, see https://api.mongodb.com/python/current/tutorial.html#querying-by-objectid
from bson.objectid import ObjectId

class NovelscrapePipeline:

    collection_name = 'novels'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        my_item = ItemAdapter(item).asdict()

        # find one document by title
        my_doc = self.db[self.collection_name].find_one({'title': my_item['title']})
        if not my_doc:
            # if there is no matched document, insert a new one
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        else:
            # update the existing document with not-none values
            self.db[self.collection_name].update(
                {'_id': ObjectId(my_doc['_id'])},
                {
                    '$set': {k: v for k, v in my_item.items() if v is not None}
                }
                )

        return item
