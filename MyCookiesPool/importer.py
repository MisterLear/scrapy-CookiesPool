# coding:utf-8

from cookiespool.db import MongoDBConfig
from cookiespool.config import COOKIES_TABLE

class Importer(object):
    def __init__(self):
        self.conn = MongoDBConfig(COOKIES_TABLE)
        doc = self.conn.find()
        print("当前数据库内有 ", len(doc), " 条数据")

    def set(self, username, password, cookies=None):
        document = {"_id": username, "password": password, "cookies": cookies}
        try:
            self.conn.insert(document)
            print('账号', username, '密码', password)
            print('录入成功')
        except:
            print('录入失败')

    def scan(self):
        while True:
            username = str(input('请输入用户名，输入exit退出读入:\n'))
            if username == 'exit':
                break
            password = str(input('请输入密码，输入exit退出读入:\n'))
            if password == 'exit':
                break
            self.set(username, password)


if __name__ == '__main__':
    Importer().scan()
    "18898730133 / 18218711823"
    "qichacha123@ / abcde@2019"