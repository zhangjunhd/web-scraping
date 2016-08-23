# -*- coding: utf-8 -*-
import random
import logging
from cookies import cookies
from user_agents import agents
from shift_queue import ShiftQueue, NormalQueue
from project_cfg import project_config


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """

    def __init__(self):
        self.logger = logging.getLogger()
        rotate_time = project_config.get_cookie_rotate_time()
        if rotate_time <= 1:
            self.cookieQueue = NormalQueue(cookies)
        else:
            self.cookieQueue = ShiftQueue(cookies, project_config.get_cookie_rotate_time())
            self.cookieQueue.start()
        self.logger.info('init worker queue size:%d, rest queue size:%d'
                         % (len(self.cookieQueue.get_work()), len(self.cookieQueue.get_rest())))

    def process_request(self, request, spider):
        cookie = random.choice(self.cookieQueue.get_work())
        request.cookies = cookie
