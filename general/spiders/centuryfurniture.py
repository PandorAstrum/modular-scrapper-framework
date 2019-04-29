# -*- coding: utf-8 -*-
import scrapy


class CenturyfurnitureSpider(scrapy.Spider):
    name = 'centuryfurniture'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        pass
