# -*- coding: utf-8 -*-
import scrapy


class SampleScrapperSpider(scrapy.Spider):
    name = 'sample_scrapper'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        pass
