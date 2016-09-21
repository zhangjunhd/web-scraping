# -*- coding: utf-8 -*-
from urlparse import urljoin
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
from alexa.items import Site


class Alexa(CrawlSpider):
    name = "alexa"
    host = "http://www.alexa.com"
    start_urls = [
        'Health', 'Reference', 'Sports', 'Arts', 'Home', 'Regional', 'Business', 'Kids_and_Teens',
        'Science', 'Computers', 'News', 'Shopping', 'Games', 'Recreation', 'Society',
    ]
    categories = set(start_urls)

    def __init__(self, *a, **kw):
        super(Alexa, self).__init__(*a, **kw)

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
                site = Site()
                site['_id'] = url_part.split('/')[2]
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
