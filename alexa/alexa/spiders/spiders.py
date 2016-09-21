# -*- coding: utf-8 -*-
from urlparse import urljoin
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
from alexa.items import Site
from alexa.check_item import finish


class Alexa(CrawlSpider):
    name = "alexa"
    host = "http://www.alexa.com"
    start_urls = [
        'Health', 'Reference', 'Sports', 'Arts', 'Home', 'Regional', 'Business', 'Kids_and_Teens',
        'Science', 'Computers', 'News', 'Shopping', 'Games', 'Recreation', 'Society', 'Adult'
    ]
    categories = set(start_urls)

    def __init__(self, *a, **kw):
        super(Alexa, self).__init__(*a, **kw)
        self.finished = finish()
        self.logger.info('total load finished url : %d' % len(self.finished))

    def start_requests(self):
        while len(self.categories) > 0:
            category = self.categories.pop()

            # http://www.alexa.com/topsites/category/Top/Health
            # http://www.alexa.com/topsites/category;1/Top/Health
            # http://www.alexa.com/topsites/category;19/Top/Health
            url_category = "http://www.alexa.com/topsites/category/Top/%s" % category
            self.logger.info('generate category url:%s' % url_category)
            yield Request(url=url_category, meta={"category": category}, callback=self.parse_category)
            for idx in xrange(1, 20):
                url_category = "http://www.alexa.com/topsites/category;%d/Top/%s" % (idx, category)
                self.logger.info('generate category url:%s' % url_category)
                yield Request(url=url_category, meta={"category": category}, callback=self.parse_category)
        url_listing = "http://www.alexa.com/topsites"
        self.logger.info('generate category url:%s' % url_listing)
        yield Request(url=url_listing, meta={"category": "World"}, callback=self.parse_listing)
        for idx in xrange(1, 20):
            url_listing = "http://www.alexa.com/topsites/global;%d" % idx
            self.logger.info('generate category url:%s' % url_listing)
            yield Request(url=url_listing, meta={"category": "World"}, callback=self.parse_listing)

    def parse_listing(self, response):
        selector = Selector(response)
        text_list = selector.xpath('body//section[@class="td col-r"]/div[@class="listings"]/ul').extract()
        text = text_list[0]
        bs = BeautifulSoup(text, 'lxml')

        for ul in bs.findAll('ul'):
            for li in ul.findAll('li'):
                url_part = li.a.get('href')  # /siteinfo/google.com
                url_key = url_part.split('/')[2]
                if url_key in self.finished:
                    self.logger.info('skip url:%s' % url_key)
                    continue

                site = Site()
                site['_id'] = url_key
                site['category'] = response.meta["category"]
                site['desc'] = li.find("div", {"class": "description"}).contents[0].strip()
                url_detail = urljoin('http://www.alexa.com', url_part)
                site['url'] = url_detail
                self.logger.info('generate detail url:%s' % url_detail)
                yield Request(url=url_detail, meta={"item": site}, callback=self.parse_detail)

    def parse_category(self, response):
        # debug with scrapy.shell
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        selector = Selector(response)
        text_list = selector.xpath('body//section[@class="td col-r"]/ul').extract()
        text = text_list[0]
        bs = BeautifulSoup(text, 'lxml')

        for ul in bs.findAll('ul'):
            for li in ul.findAll('li'):
                url_part = li.a.get('href')  # /siteinfo/google.com
                url_key = url_part.split('/')[2]
                if url_key in self.finished:
                    self.logger.info('skip url:%s' % url_key)
                    continue

                site = Site()
                site['_id'] = url_key
                site['category'] = response.meta["category"]
                site['desc'] = li.find("div", {"class": "description"}).contents[0].strip()
                url_detail = urljoin('http://www.alexa.com', url_part)
                site['url'] = url_detail
                self.logger.info('generate detail url:%s' % url_detail)
                yield Request(url=url_detail, meta={"item": site}, callback=self.parse_detail)

    def parse_detail(self, response):
        site = response.meta["item"]
        selector = Selector(response)
        text_list = selector.xpath('//span[@class="globleRank"]//strong[@class="metrics-data align-vmiddle"]').extract()
        text = text_list[0]
        bs = BeautifulSoup(text, 'lxml')
        site['global_rank'] = int(bs.strong.get_text().strip().replace(',', ''))
        yield site
