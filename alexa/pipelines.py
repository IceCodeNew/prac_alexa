# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy.utils.project import get_project_settings


class AlexaPipeline(object):
    def __init__(self):
        sql = get_project_settings()

        self.conn = MySQLdb.connect(host=sql["MYSQL_HOST"], port=sql["MYSQL_PORT"], user=sql["MYSQL_USER"],
                                    passwd=sql["MYSQL_PASSWD"], db=sql["MYSQL_DB"], charset=sql["MYSQL_CHARSET"])
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        def getmytuple(rank: int, domain: str, desc: str):
            tup = (rank, domain, desc)
            return tup

        mylist = []
        for i in range(len(item["desc"])):
            mylist.append(getmytuple(item["rank"][i], item["domain"][i], item["desc"][i]))
        sqlcommand = "INSERT INTO `info` (`rank`, `domain`, `desc`) VALUES (%s, %s, %s)"
        self.cursor.executemany(sqlcommand, mylist)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
