# -*- coding: utf-8 -*-
import scrapy


class SampleSpiderSpider(scrapy.Spider):
    name = 'sample_spider'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        pass
