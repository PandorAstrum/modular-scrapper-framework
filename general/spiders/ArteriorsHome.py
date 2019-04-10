# -*- coding: utf-8 -*-
import scrapy


class ArteriorshomeSpider(scrapy.Spider):
    name = 'ArteriorsHome'
    allowed_domains = ['www.arteriorshome.com']
    start_urls = ['http://www.arteriorshome.com/']

    def parse(self, response):
        pass
