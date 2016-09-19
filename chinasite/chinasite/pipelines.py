# -*- coding: utf-8 -*-
import pymongo
from items import Site

DB_URL = 'localhost'
DB_PORT = 27017
DB_NAME = 'chinasite'
COLLECTION_SITE = 'Site'


class MongoDB(object):
    def __init__(self):
        client = pymongo.MongoClient(DB_URL, DB_PORT)
        db = client[DB_NAME]
        self.collection = db[COLLECTION_SITE]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, Site):
            try:
                self.collection.insert(dict(item))
            except Exception, e:
                print e
        return item
