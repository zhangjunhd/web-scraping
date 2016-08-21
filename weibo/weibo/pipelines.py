# -*- coding: utf-8 -*-
import pymongo
from project_cfg import project_config
from items import InformationItem, WeibosItem, FollowsItem, FansItem


class MongoDBTopology(object):
    def __init__(self):
        client = pymongo.MongoClient(project_config.get_database_url(), project_config.get_database_port())
        db = client["Sina"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, FollowsItem):
            followsItems = dict(item)
            follows = followsItems.pop("follows")
            for i in range(len(follows)):
                followsItems[str(i + 1)] = follows[i]
            try:
                self.Follows.insert(followsItems)
            except Exception, e:
                print e
        elif isinstance(item, FansItem):
            fansItems = dict(item)
            fans = fansItems.pop("fans")
            for i in range(len(fans)):
                fansItems[str(i + 1)] = fans[i]
            try:
                self.Fans.insert(fansItems)
            except Exception, e:
                print e
        return item


class MongoDB(object):
    def __init__(self):
        client = pymongo.MongoClient(project_config.get_database_url(), project_config.get_database_port())
        db = client["Sina"]
        self.Information = db["Information"]
        self.Weibo = db["Weibo"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]

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
