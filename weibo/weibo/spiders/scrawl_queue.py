# -*- coding: utf-8 -*-
import threading
from weibo.project_cfg import project_config
from weibo.pipelines import COLLECTION_FOLLOW, COLLECTION_FAN, COLLECTION_INFORMATION
from weibo.logutil import Logging
import pymongo


class ScrawlQueue(object):

    def __init__(self):
        self.logger = Logging.get_logger()
        self.scrawl_lock = threading.Lock()
        self.finish_lock = threading.Lock()
        self.scrawl_ID = set()  # 记录待爬的微博ID
        self.finish_ID = set()  # 记录已爬的微博ID
        self._init_load()

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

    def _init_load(self):
        # load from database
        client = pymongo.MongoClient(project_config.get_database_url(), project_config.get_database_port())
        self.db = client[project_config.get_database_name()]
        self._fill_from_collection(COLLECTION_FOLLOW)
        self._fill_from_collection(COLLECTION_FAN)
        self._fill_from_start_url()
        self.scrawl_ID -= self.finish_ID
        self.logger.info('finish fill finish_ID:%d,scrawl_ID:%d' % (len(self.finish_ID), len(self.scrawl_ID)))

    def _fill_from_collection(self, collection):
        cursor = self.db.get_collection(collection).find()
        for document in cursor:
            self.finish_ID.add(document['_id'])
            for idx in range(1, len(document)):
                self.scrawl_ID.add(document[str(idx)])
        self.logger.info('fill finish_ID:%d,scrawl_ID:%d' % (len(self.finish_ID), len(self.scrawl_ID)))

    def _fill_from_start_url(self):
        # check queue empty
        if len(self.scrawl_ID) == 0:
            start_urls = project_config.get_start_accounts()
            self.scrawl_ID = set(start_urls)
            self.logger.info('finish fill scrawl_ID:%d' % len(self.scrawl_ID))


if __name__ == "__main__":
    q = ScrawlQueue()
