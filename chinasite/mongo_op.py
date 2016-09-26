# coding:utf-8
import sys
import string
import pymongo

reload(sys)
sys.setdefaultencoding('utf8')


HOST = 'localhost'


def int_rank(tpe):
    client = pymongo.MongoClient(host=HOST)
    db = client.chinasite
    update_number = 0
    for record in db.Site.find({"type": tpe}):
        # record['region_rank'] = int(record['region_rank'])
        # record['total_rank'] = int(record['total_rank'])
        # record['type_rank'] = int(record['type_rank'])
        record['alexa'] = int(record['alexa'])
        db.Site.save(record)
        update_number += 1
        print record['_id']
    return update_number


def fillna_rank(rank_item="region_rank", rank_val=None):
    client = pymongo.MongoClient(host=HOST)
    db = client.chinasite
    for record in db.Site.find({rank_item: rank_val}):
        record[rank_item] = 0
        db.Site.save(record)
        print record['_id']


def check_rank(rank_item="region_rank", rank_val=None):
    client = pymongo.MongoClient(host=HOST)
    db = client.chinasite
    results = db.Site.find({rank_item: rank_val})
    for item in results:
        print item


def size_check_rank(rank_item="region_rank", rank_val=None):
    client = pymongo.MongoClient(host=HOST)
    db = client.chinasite
    return db.Site.find({rank_item: rank_val}).count()


def check_all_rank():
    print 'total_rank=0     %d' % size_check_rank(rank_item="total_rank", rank_val=0)
    print 'total_rank=None  %d' % size_check_rank(rank_item="total_rank", rank_val=None)
    print 'region_rank=0    %d' % size_check_rank(rank_val=0)
    print 'region_rank=None %d' % size_check_rank(rank_val=None)
    print 'type_rank=0      %d' % size_check_rank(rank_item="type_rank", rank_val=0)
    print 'type_rank=None   %d' % size_check_rank(rank_item="type_rank", rank_val=None)


def list_type():
    client = pymongo.MongoClient(host=HOST)
    db = client.chinasite
    return db.Site.distinct("type")


def list_subtype(tpe):
    client = pymongo.MongoClient(host=HOST)
    db = client.chinasite
    results = db.Site.aggregate([
        {"$match": {'type': tpe}},
        {"$group": {"_id": "$subtype"}}
    ])
    subtpes = []
    for item in results:
        subtpes.append(item['_id'])
    return subtpes


def sort_by_type(tpe, rank_by="total_rank", limit_size=100):
    client = pymongo.MongoClient(host=HOST)
    db = client.chinasite
    results = db.Site.find({"type": tpe, rank_by: {"$ne": 0}}).sort([(rank_by, 1)]).limit(limit_size)
    return results


def markdown(content_dict, type):
    contents = ['#站长之家网站统计:%s' % type]
    contents.extend(['| Title | Region | Rank | Alexa |',
                     '| --- | --- | --- | --- |'])
    for item in content_dict:
        #    if item['description'] is None:
        #        desc = 'N/A'
        #    else:
        #        desc = string.replace(item['description'], '\n', '')
            contents.append('| [%s](http://%s) | %s | %s | %s |' % (
                item['title'],
                item['_id'],
                item['region'],
                item['total_rank'],
                item['alexa']))

    file_object = open('site.md', 'w')
    file_object.write('\n'.join(contents))
    file_object.close()

if __name__ == '__main__':
    results = sort_by_type("购物网站")
    markdown(results, "购物网站")

'''
综合其他 8751
休闲娱乐 8387
新闻媒体 1694
生活服务 8745
行业企业 4385
体育健身 754
网络科技 3219
医疗健康 1304
教育文化 6415
交通旅游 1725
购物网站 2232
政府组织 3074
'''