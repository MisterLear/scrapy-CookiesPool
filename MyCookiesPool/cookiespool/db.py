# coding:utf-8

import pymongo
from cookiespool.config import MONGODB_PORT, MONGODB, MONGODB_HOST


class MongoDBConfig(object):
    def __init__(self, TABLE):
        # MondoDB 数据连接
        self.client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
        # 选择或创建数据库
        self.db = self.client[MONGODB]
        # 选择或创建数据储存表
        self.collection = self.db[TABLE]

    def insert(self, document):
        self.collection.insert_one(document)

    def update(self, filter, update, upsert):
        self.collection.update(filter, update, upsert)

    def find(self, where=None):
        doc = self.collection.find(where)
        return [each for each in doc]

    def count(self, where=None):
        self.collection.find(where).count()

    def delete(self, where, justOne=None):
        self.collection.remove(where, justOne)
