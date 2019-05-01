# -*- coding: utf-8 -*-
import random
import re

import scrapy
from loginform import fill_login_form
from scrapy import Request, FormRequest

from general.items import ProductItems, PriceItems

class VanguardfurnitureSpider(scrapy.Spider):
    name = 'vanguardfurniture'
    allowed_domains = ['www.google.com']
    def __init__(self, **kwargs):
        super(VanguardfurnitureSpider, self).__init__(**kwargs)
        self._username = kwargs.get("_username")
        self._password = kwargs.get("_password")
        self._login = kwargs.get("_signin")
        self.customer_id = kwargs.get("_customerid")
        self._take_price = False
        self.start_urls = ["https://www.hookerfurniture.com/livingroom.inc"]
        self.siteID = 9
        self.login_url = "http://elink.hookerfurniture.com/"
        self.headers_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
            "Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0"]

        if self._login == "True":
            self._login = True
            self._take_price = self._login
        elif self._login == "False":
            self._login = False
            self._take_price = self._login
        self.header = random.choice(self.headers_pool)

    def start_requests(self):
        if self._login:
            yield Request(self.login_url, headers={'User-Agent': self.header})
        else:
            for url in self.start_urls:
                yield Request(url, headers={'User-Agent': self.header})

    def parse(self, response):
        if self._login:
            # fill login form
            data, url, method = fill_login_form(response.url, response.body,
                                                self._username, self._password)
            # send a request with our login data
            yield FormRequest(url, formdata=dict(data),
                              method=method, callback=self.parse_after_login,
                              headers={'User-Agent': self.header})
        else:
            _all_sub_category = response.xpath('//ul[@class="DepartmentAttributeListClass"]/li/a/@href').extract()
            if len(_all_sub_category) <= 0:
                pass
            else:
                for _sub_category_link in _all_sub_category:
                    abs_sub_category_link = response.urljoin(_sub_category_link)
                    yield Request(url=abs_sub_category_link, callback=self.parse_deep,
                                      headers={'User-Agent': self.header})

    def parse_after_login(self, response):
        self._login = False
        print("logged in")
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': self.header})

    def parse_deep(self, response):
        # grab total item
        _total_item_count = response.xpath('//div[@class="TotalItemCount"]/p/text()').extract_first()
        _item_amount_int = int(re.sub(r'([i|I]tem\(s\)|[i|I]tems?)', '', _total_item_count).strip())
        # calculate how many ajax call required
        _total_times_to_call_ajax = []
        for i in range(0, _item_amount_int, 12):
            _total_times_to_call_ajax.append(i)
        # Ajax Call Build up
        for j in _total_times_to_call_ajax:
            make_url_with_ajax = response.url + f"&_offs={j}"
            yield Request(url=make_url_with_ajax, callback=self.parse_item_links,
                          headers={'User-Agent': self.header})

    def parse_item_links(self, response):
        _all_item_links = response.xpath('//p[@class="ProductThumbnailParagraph ProductThumbnailParagraphDescription"]/a/@href').extract()
        for _item_link in _all_item_links:
            abs_item_link = response.urljoin(_item_link)
            yield Request(url=abs_item_link, callback=self.parse_item,
                          headers={'User-Agent': self.header})

    def parse_item(self, response):
        print(f"grabbing item {response.url}")
        _category = response.meta['cat']
        # grab actual data here
        if not self._take_price:
            _productItem = ProductItems()
            item_name = response.xpath('//div[@id="item-info-short-description"]/h1/text()').extract_first()
            if not item_name:
                item_name = ""
            sku = response.xpath('//span[@id="spansku"]/text()').extract_first()
            if not sku:
                sku = ""
            item_description = response.xpath('//div[@id="description"]/text()').extract_first()
            if not item_description:
                item_description = ""
            d = response.xpath(
                '//li[@id="dimensions"]/span[@class="data"]/span[@class="product-diamen"]/text()').extract()
            if len(d) <= 0:
                dimension = f"Dimension Xpath Changed at {response.url}"
            else:
                dimension = ', '.join(d)
            photos = response.xpath('//li[@class="item"]/a/img/@src').extract()
            if len(photos) <= 0:
                photos = []

            _productItem['SiteId'] = self.siteID
            _productItem['SKU'] = sku
            _productItem['ItemName'] = item_name
            _productItem['Category'] = _category
            _productItem['URL'] = response.url
            _productItem['ItemDescription'] = item_description
            _productItem['Dimension'] = dimension
            _productItem['Photos'] = photos
            yield _productItem
        else:
            _priceItem = PriceItems()
            _sku = response.xpath('//span[@id="spansku"]/text()').extract_first()
            if not _sku:
                _sku = ""
            _msrp = response.xpath('//p[@class="sugested-price "]/span[@class="price"]/text()').extract_first()
            if not _msrp:
                _msrp = ""
            _net = response.xpath('//p[@class="normal-price"]/span[@class="price"]/text()').extract_first()
            if not _net:
                _net = ""

            _priceItem["SKU"] = _sku
            _priceItem["MSRP"] = _msrp
            _priceItem["NET"] = _net
            _priceItem["CUSTOMERID"] = self.customer_id
            yield _priceItem
