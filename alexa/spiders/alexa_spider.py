# 备忘 By ICN
# 如在 import win32api 时报错“找不到指定的模块”，在 python 安装目录中执行以下语句：
# python scripts\pywin32_postinstall.py -install

import re
from typing import List

import scrapy

from alexa.items import AlexaItem


def getlist(selectorlist: scrapy.selector.unified.SelectorList):
    pattern1 = re.compile(r'^\s+|\s+$|\\[rn]', re.MULTILINE)
    pattern2 = re.compile(r'\s{2,}', re.MULTILINE)
    pattern3 = re.compile(r'\"{3,}', re.MULTILINE)

    tmp_list: List = selectorlist.xpath('string(.)').extract()
    mylist = [
        pattern3.sub(
            r'""', pattern2.sub(r' ', pattern1.sub(r'', _.replace('"', '""')))
        )
        for _ in tmp_list
    ]
    del tmp_list
    return mylist


class AlexaSpider(scrapy.spiders.Spider):
    name = 'alexa'
    allowed_domains = ['chinaz.com']

    start_urls = ['http://alexa.chinaz.com/Country/index_CN.html']
    for i in range(1, 20):
        url = 'http://alexa.chinaz.com/Country/index_CN_{index}.html'''.format(index=str(i + 1))
        start_urls.append(url)

    def parse(self, response):
        item = AlexaItem()

        clearfix = response.xpath('//li[@class="clearfix"]')
        item['rank'] = getlist(clearfix.xpath('.//div[@class="count"]'))
        item['domain'] = getlist(clearfix.xpath('.//span'))
        item['desc'] = getlist(clearfix.xpath('.//p[@class=""]'))

        return item
