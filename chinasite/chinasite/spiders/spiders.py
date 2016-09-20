# -*- coding: utf-8 -*-
from urlparse import urljoin
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
from chinasite.items import Site


class ChinaSite(CrawlSpider):
    name = "chinasite"
    host = "http://top.chinaz.com"

    def __init__(self, *a, **kw):
        super(ChinaSite, self).__init__(*a, **kw)

    def start_requests(self):
        yield Request(url='http://top.chinaz.com/all/index.html', callback=self.parse_rank)
        total_page = 1730
        cur_idx = 2

        while cur_idx <= total_page:
            url = 'http://top.chinaz.com/all/index_%d.html' % cur_idx
            self.logger.info('generate index url:%s' % url)
            yield Request(url=url, callback=self.parse_rank)
            cur_idx += 1

    def parse_rank(self, response):
        selector = Selector(response)
        text_list = selector.xpath(
            'body/div[@class="Wrapper"]/div[@class="TopListCent"]/div[@class="TopListCent-listWrap"]/ul').extract()
        text = text_list[0]
        bs = BeautifulSoup(text, 'lxml')
        for ul in bs.findAll('ul'):
            for li in ul.findAll('li'):
                href = li.div.a.get('href')  # /Html/site_ctrip.com.html
                site = Site()
                site['img'] = li.div.img.get('src')  # http://pic.top.chinaz.com/WebSiteimages/ctripcom/ced38a12-2.png
                site['title'] = li.div.find_next_siblings("div")[0].a.get('title')  # 携程旅行网
                site['_id'] = li.div.find_next_siblings("div")[0].span.string     # ctrip.com
                site['alexa'] = li.div.find_next_siblings("div")[0].div.a.string  # Alexa周排名
                url_detail = urljoin('http://top.chinaz.com/', href)
                site['url'] = url_detail
                self.logger.info('generate detail url:%s' % url_detail)
                yield Request(url=url_detail, meta={"item": site}, callback=self.parse_detail)

    def parse_detail(self, response):
        site = response.meta["item"]
        ranks = ['total_rank', 'region_rank', 'type_rank']

        selector = Selector(response)
        text_list = selector.xpath(
            'body/div[@class="TPmain"]//div[@class="Tagone TopMainTag-show"]').extract()
        text = text_list[0]
        bs = BeautifulSoup(text, 'lxml')
        # 网站类型
        if bs.p.a is not None:
            site['type'] = bs.p.a.string  # 网络科技/综合其他
            if len(bs.p.a.find_next_siblings("a")) >= 1:
                site['subtype'] = bs.p.a.find_next_siblings("a")[0].string  # 电脑硬件/门户网站
            if len(bs.p.a.find_next_siblings("a")) >= 3:
                site['type2'] = bs.p.a.find_next_siblings("a")[1].string  # 新闻媒体
                site['subtype2'] = bs.p.a.find_next_siblings("a")[2].string  # 新闻报刊
        else:
            site['type'] = None
            site['subtype'] = None

        # 所属区域
        site['region'] = bs.p.find_next_siblings("p")[0].a.string  # 北京
        if len(bs.p.find_next_siblings("p")) >= 2:
            site['subregion'] = bs.p.find_next_siblings("p")[1].a.string  # 东城区

        # 排名
        text_list2 = selector.xpath(
            'body/div[@class="TPmain"]//div[@class="TPageCent-TopMain mt10 clearfix"]/ul').extract()
        text2 = text_list2[0]
        bs2 = BeautifulSoup(text2, 'lxml')
        for ul in bs2.findAll('ul'):
            rank_loc = 0
            for li in ul.findAll('li'):
                if li.a is not None:
                    site[ranks[rank_loc]] = int(li.a.string)
                else:
                    site[ranks[rank_loc]] = 0
                rank_loc += 1

        # 站点介绍
        text_list3 = selector.xpath('body/div[@class="TPmain"]//div[@class="Centright fr SimSun"]').extract()
        text3 = text_list3[0]
        bs3 = BeautifulSoup(text3, 'lxml')
        site['description'] = bs3.p.string
        yield site

