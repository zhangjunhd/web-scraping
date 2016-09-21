# -*- coding: utf-8 -*-
from scrapy import Item, Field


class Site(Item):
    _id = Field()
    url = Field()
    category = Field()
    desc = Field()
    global_rank = Field()
