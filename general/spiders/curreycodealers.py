# -*- coding: utf-8 -*-
import scrapy


class CurreycodealersSpider(scrapy.Spider):
    name = 'curreycodealers'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        pass
