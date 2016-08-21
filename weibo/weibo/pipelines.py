# -*- coding: utf-8 -*-
import pymongo
from project_cfg import project_config
from items import InformationItem, WeibosItem, FollowsItem, FansItem


COLLECTION_FOLLOW = 'Follows'
COLLECTION_FAN = 'Fans'
COLLECTION_INFORMATION = 'Information'
COLLECTION_WEIBO = 'Weibo'


class MongoDB(object):
    def __init__(self):
        client = pymongo.MongoClient(project_config.get_database_url(), project_config.get_database_port())
        db = client[project_config.get_database_name()]
        self.Information = db[COLLECTION_INFORMATION]
        self.Weibo = db[COLLECTION_WEIBO]
        self.Follows = db[COLLECTION_FOLLOW]
        self.Fans = db[COLLECTION_FAN]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception, e:
                print e
        elif isinstance(item, WeibosItem):
            try:
                self.Weibo.insert(dict(item))
            except Exception, e:
                print e
        elif isinstance(item, FollowsItem):
            follows_item = dict(item)
            follows = follows_item.pop("follows")
            for i in range(len(follows)):
                follows_item[str(i + 1)] = follows[i]
            try:
                self.Follows.insert(follows_item)
            except Exception, e:
                print e
        elif isinstance(item, FansItem):
            fans_item = dict(item)
            fans = fans_item.pop("fans")
            for i in range(len(fans)):
                fans_item[str(i + 1)] = fans[i]
            try:
                self.Fans.insert(fans_item)
            except Exception, e:
                print e
        return item
