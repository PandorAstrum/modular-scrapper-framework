# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Spider
from general.items import GeneralItem

class ArteriorshomeSpider(Spider):
    name = 'ArteriorsHome'
    allowed_domains = ['www.arteriorshome.com']

    def __init__(self, **kwargs):
        super(ArteriorshomeSpider, self).__init__(**kwargs)
        self.start_urls = kwargs.get('_start_urls')
        self.headers = kwargs.get('_headers')
        self.login = kwargs.get('_login')
        self.username = kwargs.get('_username')
        self.password = kwargs.get('_pass')
        self.take_price = kwargs.get('_take_price')
        self.login_url = kwargs.get('_login_url')
        self.siteID = kwargs.get('_siteId')
        self.tmp_links = []

    def start_requests(self):
        if self.take_price:
            # self.login_url utilize it
            pass # login here
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': self.headers})

    def parse(self, response):
        # get only categories link
        all = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()

        for a in all:
            yield Request(url=a, callback=self.parse2, headers={'User-Agent': self.headers})

    def parse2(self, response):
        # get sub categories link
        all = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()

        for a in all:
            yield Request(url=a, callback=self.parse3, headers={'User-Agent': self.headers})

    def parse3(self, response):
        # load all items and get links
        _item_amount = response.xpath('//div[@class="pager"]/p/text()').extract_first()
        _item_amount = _item_amount.replace('items', '').strip()
        ajax_req = "p=16&is_ajax=1"
        _total_length = []
        for i in range(0, int(_item_amount), 20):
            _total_length.append(i)

        for j in range(0, len(_total_length)+1):
            make_url_with_ajax = response.url + f"p={i}&is_ajax=1"
            yield Request(url=make_url_with_ajax, callback=self.parse4, headers={'User-Agent': self.headers})

    def parse4(self, response):
        # grab item link
        item_links = response.xpath('//li[@class="item"]/a/@href').extract()
        for item in item_links:
            yield Request(url=item, callback=self.parse5, headers={'User-Agent': self.headers})

    def parse5(self, response):
        item = GeneralItem()
        # grab actual data here

        ItemName = response.xpath('//div[@class="product-name"]/h1/text()').extract_first()
        SKU = response.xpath('//span[@id="spansku"]/text()').extract_first()
        ItemDescription = response.xpath('//div[@id="description"]/text()').extract_first()
        d = response.xpath('//li[@id="dimensions"]/span[@class="data"]/span[@class="product-diamen"]/text()').extract()
        Dimension = ', '.join(d)
        Photos = response.xpath('//li[@class="item"]/a/img/@src').extract()
        SiteId = self.siteID
