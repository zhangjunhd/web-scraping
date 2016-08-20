# -*- coding: utf-8 -*-
BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

DOWNLOADER_MIDDLEWARES = {
    "weibo.middleware.UserAgentMiddleware": 401,
    "weibo.middleware.CookiesMiddleware": 402,
}

ITEM_PIPELINES = {
    'weibo.pipelines.MongoDBTopology': 300,
}

DOWNLOAD_DELAY = 1  # 间隔时间
# CONCURRENT_ITEMS = 1000
# CONCURRENT_REQUESTS = 100
# REDIRECT_ENABLED = False
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 0
# CONCURRENT_REQUESTS_PER_SPIDER=100
# DNSCACHE_ENABLED = True
# LOG_LEVEL = 'INFO'    # 日志级别
# CONCURRENT_REQUESTS = 70
