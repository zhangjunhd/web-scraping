# coding:utf-8
import pymongo

HOST = 'localhost'


def finish(debug=False):
    finished = set()
    client = pymongo.MongoClient(host=HOST)
    db = client.alexa
    for record in db.Site.find():
        url_id = record['_id']
        finished.add(url_id)
        if debug:
            print url_id
    return finished

if __name__ == '__main__':
    size = len(finish(debug=True))
    print 'finish size:%d' % size

