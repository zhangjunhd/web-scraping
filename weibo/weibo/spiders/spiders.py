# -*- coding: utf-8 -*-
import re
import datetime
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from weibo.items import InformationItem, WeibosItem, FollowsItem, FansItem
from scrawl_queue import ScrawlQueue


class Weibo(CrawlSpider):
    name = "weibo"
    host = "http://weibo.cn"

    def __init__(self, *a, **kw):
        super(Weibo, self).__init__(*a, **kw)
        self.queue = ScrawlQueue()

    def start_requests(self):
        while True:
            item = self.queue.pop_scrawl()
            self.queue.push_finish(item)  # 加入已爬队列
            follows = []
            follows_item = FollowsItem()
            follows_item["_id"] = str(item)
            follows_item["follows"] = follows
            fans = []
            fans_item = FansItem()
            fans_item["_id"] = str(item)
            fans_item["fans"] = fans

            url_follows = "http://weibo.cn/%s/follow" % str(item)
            url_fans = "http://weibo.cn/%s/fans" % str(item)
            url_weibos = "http://weibo.cn/%s/profile?filter=1&page=1" % str(item)
            url_information = "http://weibo.cn/attgroup/opening?uid=%s" % str(item)

            yield Request(url=url_follows, meta={"item": follows_item, "result": follows},
                          callback=self.parse_follow_or_fan)  # 去爬关注人
            yield Request(url=url_fans, meta={"item": fans_item, "result": fans},
                          callback=self.parse_follow_or_fan)  # 去爬粉丝
            # yield Request(url=url_information, meta={"ID": ID}, callback=self.parse_person_info)  # 去爬个人信息
            # yield Request(url=url_weibos, meta={"ID": ID}, callback=self.parse2)  # 去爬微博

    def parse_person_info(self, response):
        """ 抓取个人信息1 """
        info_item = InformationItem()
        selector = Selector(response)
        text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
        if text0:
            num_weibos = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)  # 微博数
            num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
            num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数
            if num_weibos:
                info_item["Num_Weibos"] = int(num_weibos[0])
            if num_follows:
                info_item["Num_Follows"] = int(num_follows[0])
            if num_fans:
                info_item["Num_Fans"] = int(num_fans[0])
                info_item["_id"] = response.meta["ID"]
            url_information1 = "http://weibo.cn/%s/info" % response.meta["ID"]
            yield Request(url=url_information1, meta={"item": info_item}, callback=self.parse_person_info_ext)

    @staticmethod
    def parse_person_info_ext(response):
        """ 抓取个人信息2 """
        info_item = response.meta["item"]
        selector = Selector(response)
        text1 = ";".join(selector.xpath('body/div[@class="c"]/text()').extract())  # 获取标签里的所有text()
        nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', text1)  # 昵称
        gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', text1)  # 性别
        place = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', text1)  # 地区（包括省份和城市）
        signature = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 个性签名
        birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
        sexorientation = re.findall(u'\u6027\u53d6\u5411[:|\uff1a](.*?);', text1)  # 性取向
        marriage = re.findall(u'\u611f\u60c5\u72b6\u51b5[:|\uff1a](.*?);', text1)  # 婚姻状况
        url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接

        if nickname:
            info_item["NickName"] = nickname[0]
        if gender:
            info_item["Gender"] = gender[0]
        if place:
            place = place[0].split(" ")
            info_item["Province"] = place[0]
            if len(place) > 1:
                info_item["City"] = place[1]
        if signature:
            info_item["Signature"] = signature[0]
        if birthday:
            try:
                birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                info_item["Birthday"] = birthday - datetime.timedelta(hours=8)
            except Exception, e:
                print e
        if sexorientation:
            if sexorientation[0] == gender[0]:
                info_item["Sex_Orientation"] = "gay"
            else:
                info_item["Sex_Orientation"] = "Heterosexual"
        if marriage:
            info_item["Marriage"] = marriage[0]
        if url:
            info_item["URL"] = url[0]
        yield info_item

    def parse2(self, response):
        """ 抓取微博数据 """
        selector = Selector(response)
        weibos = selector.xpath('body/div[@class="c" and @id]')
        for weibo in weibos:
            weibosItems = WeibosItem()
            id = weibo.xpath('@id').extract_first()  # 微博ID
            content = weibo.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
            cooridinates = weibo.xpath('div/a/@href').extract_first()  # 定位坐标
            like = re.findall(u'\u8d5e\[(\d+)\]', weibo.extract())  # 点赞数
            transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', weibo.extract())  # 转载数
            comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', weibo.extract())  # 评论数
            others = weibo.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）

            weibosItems["ID"] = response.meta["ID"]
            weibosItems["_id"] = response.meta["ID"] + "-" + id
            if content:
                weibosItems["Content"] = content.strip(u"[\u4f4d\u7f6e]")  # 去掉最后的"[位置]"
            if cooridinates:
                cooridinates = re.findall('center=([\d|.|,]+)', cooridinates)
                if cooridinates:
                    weibosItems["Co_oridinates"] = cooridinates[0]
            if like:
                weibosItems["Like"] = int(like[0])
            if transfer:
                weibosItems["Transfer"] = int(transfer[0])
            if comment:
                weibosItems["Comment"] = int(comment[0])
            if others:
                others = others.split(u"\u6765\u81ea")
                weibosItems["PubTime"] = others[0]
                if len(others) == 2:
                    weibosItems["Tools"] = others[1]
            yield weibosItems
        url_next = selector.xpath(
            u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=Weibo.host + url_next[0], meta={"ID": response.meta["ID"]}, callback=self.parse2)

    def parse_follow_or_fan(self, response):
        """ 抓取关注或粉丝 """
        items = response.meta["item"]
        selector = Selector(response)
        text2 = selector.xpath(
            u'body//table/tr/td/a[text()="\u5173\u6ce8\u4ed6" or text()="\u5173\u6ce8\u5979"]/@href').extract()
        for elem in text2:
            elem = re.findall('uid=(\d+)', elem)
            if elem:
                response.meta["result"].append(elem[0])
                item = int(elem[0])
                if not self.queue.exist_finish(item):  # 新的ID，如果未爬则加入待爬队列
                    self.queue.push_scrawl(item)
        url_next = selector.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=Weibo.host + url_next[0], meta={"item": items, "result": response.meta["result"]},
                          callback=self.parse_follow_or_fan)
        else:  # 如果没有下一页即获取完毕
            yield items
