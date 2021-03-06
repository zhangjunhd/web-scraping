# -*- coding: utf-8 -*-
BOT_NAME = 'chinasite'

SPIDER_MODULES = ['chinasite.spiders']
NEWSPIDER_MODULE = 'chinasite.spiders'

DOWNLOADER_MIDDLEWARES = {
    "chinasite.middleware.UserAgentMiddleware": 401,
}

ITEM_PIPELINES = {
    'chinasite.pipelines.MongoDB': 300,
}

DOWNLOAD_DELAY = 1  # 间隔时间
CONCURRENT_ITEMS = 32
CONCURRENT_REQUESTS = 32
# REDIRECT_ENABLED = False
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 0
# CONCURRENT_REQUESTS_PER_SPIDER=100
# DNSCACHE_ENABLED = True
# LOG_LEVEL = 'INFO'    # 日志级别
# CONCURRENT_REQUESTS = 70
