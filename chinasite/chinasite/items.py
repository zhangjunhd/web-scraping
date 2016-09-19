# -*- coding: utf-8 -*-
from scrapy import Item, Field


class Site(Item):
    _id = Field()
    img = Field()
    title = Field()
    alexa = Field()
    url = Field()
    type = Field()
    subtype = Field()
    type2 = Field()
    subtype2 = Field()
    region = Field()
    subregion = Field()
    total_rank = Field()
    region_rank = Field()
    type_rank = Field()
    description = Field()
