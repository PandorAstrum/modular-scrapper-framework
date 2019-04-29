# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime
from scrapy.exporters import JsonItemExporter


class GeneralPipeline(object):

    def get_curr_date_time(self, _strft="%Y_%b_%d_%H.%M.%S"):
        """
        functions for getting current time
        :param _strft: format to use on time
        :return: datetime now with provided format
        """
        return datetime.now().strftime(_strft)

    def open_spider(self, spider):
        self.items = []
        _path = "C:\\Users\\Ana Ash\\Desktop\\skrapy3\\project\\"
        if not spider._login:
            _path = "C:\\Users\\Ana Ash\\Desktop\\skrapy3\\project\\"
            _filename = f'{spider.name}_products_{str(self.get_curr_date_time())}.json'
        else:
            _path = "C:\\Users\\Ana Ash\\Desktop\\skrapy3\\project\\"
            _filename = f'{spider.name}_{spider.customer_id}_prices_{str(self.get_curr_date_time())}.json'
        self.file = open(_path + _filename, 'w')

    def close_spider(self, spider):
        self.file.write(json.dumps(self.items))
        self.file.close()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

