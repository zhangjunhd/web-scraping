# coding:utf-8
import pymongo

HOST = 'localhost'


def sort_by_category(category, rank_by="global_rank", limit_size=100):
    client = pymongo.MongoClient(host=HOST)
    db = client.alexa
    results = db.Site.find({"category": category, rank_by: {"$ne": 0}}).sort([(rank_by, 1)]).limit(limit_size)
    return results


def markdown(content_dict, category):
    contents = ['#Alexa Rank of Category %s' % category]
    contents.extend(['| Id | GlobalRank | Desc |',
                     '| --- | --- | --- |'])
    for item in content_dict:
            contents.append('| [%s](http://%s) | %d | %s |' % (
                item['_id'],
                item['_id'],
                item['global_rank'],
                item['desc']))

    file_object = open('alexa.md', 'w')
    file_object.write('\n'.join(contents))
    file_object.close()

if __name__ == '__main__':
    results = sort_by_category('Shopping')
    markdown(results, 'Shopping')
