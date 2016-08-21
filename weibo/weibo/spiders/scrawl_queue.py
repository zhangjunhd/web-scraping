# -*- coding: utf-8 -*-
import threading
from weibo.project_cfg import project_config
from weibo.pipelines import COLLECTION_FOLLOW, COLLECTION_FAN, COLLECTION_INFORMATION
import pymongo
import logging


class ScrawlQueue(object):

    def __init__(self):
        self.scrawl_lock = threading.Lock()
        self.finish_lock = threading.Lock()
        self.scrawl_ID = set()  # 记录待爬的微博ID
        self.finish_ID = set()  # 记录已爬的微博ID
        self.logger = logging.getLogger()

    def push_finish(self, item):
        with self.finish_lock:
            self.finish_ID.add(item)

    def pop_finish(self):
        with self.finish_lock:
            return self.finish_ID.pop()

    def exist_finish(self, item):
        with self.finish_lock:
            return item in self.finish_ID

    def push_scrawl(self, item):
        with self.scrawl_lock:
            self.scrawl_ID.add(item)

    def pop_scrawl(self):
        with self.scrawl_lock:
            return self.scrawl_ID.pop()

    def scrawl_length(self):
        with self.scrawl_lock:
            return len(self.scrawl_ID)

    def init(self):
        # load from database
        client = pymongo.MongoClient(project_config.get_database_url(), project_config.get_database_port())
        db = client[project_config.get_database_name()]
        if project_config.scrawl_fan_and_follow():
            self._fill_from_collection(db, COLLECTION_FOLLOW)
            self._fill_from_collection(db, COLLECTION_FAN)
        else:
            self._fill_from_collection2(db)
        self._fill_from_start_url()
        self.scrawl_ID -= self.finish_ID
        self.logger.info('finish fill finish_ID size:%d,scrawl_ID size:%d' % (len(self.finish_ID), len(self.scrawl_ID)))

    def _fill_from_collection(self, database, collection):
        cursor = database.get_collection(collection).find()
        for document in cursor:
            self.finish_ID.add(int(document['_id']))
            for idx in range(1, len(document)):
                self.scrawl_ID.add(int(document[str(idx)]))
        self.logger.info('fill from database finish_ID size:%d,scrawl_ID size:%d' %
                         (len(self.finish_ID), len(self.scrawl_ID)))

    def _fill_from_collection2(self, database):
        cursor = database.get_collection(COLLECTION_INFORMATION).find()
        for document in cursor:
            self.finish_ID.add(int(document['_id']))
        cursor = database.get_collection(COLLECTION_FOLLOW).find()
        for document in cursor:
            self.scrawl_ID.add(int(document['_id']))
            for idx in range(1, len(document)):
                self.scrawl_ID.add(int(document[str(idx)]))
        cursor = database.get_collection(COLLECTION_FAN).find()
        for document in cursor:
            self.scrawl_ID.add(int(document['_id']))
            for idx in range(1, len(document)):
                self.scrawl_ID.add(int(document[str(idx)]))
        self.logger.info('fill from database finish_ID size:%d,scrawl_ID size:%d' %
                         (len(self.finish_ID), len(self.scrawl_ID)))

    def _fill_from_start_url(self):
        # check queue empty
        if len(self.scrawl_ID) == 0:
            start_urls = project_config.get_start_accounts()
            self.scrawl_ID = set(start_urls)
            self.logger.info('fill from start urls scrawl_ID size:%d' % len(self.scrawl_ID))


if __name__ == "__main__":
    q = ScrawlQueue()
    q.init()
    print 'scrawl size:%d' % q.scrawl_length()
