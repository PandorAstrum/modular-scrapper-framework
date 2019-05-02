# -*- coding: utf-8 -*-
import random
import re

import scrapy
from loginform import fill_login_form
from scrapy import Request, FormRequest, Spider
from general.items import ProductItems, PriceItems


class ReginaandrewSpider(Spider):
    name = 'reginaandrew'
    allowed_domains = ['www.reginaandrew.com']

    def __init__(self, **kwargs):
        super(ReginaandrewSpider, self).__init__(**kwargs)
        self._username = kwargs.get("_username")
        self._password = kwargs.get("_password")
        self._login = kwargs.get("_signin")
        self.customer_id = kwargs.get("_customerid")
        self._take_price = False
        self.start_urls = ["https://www.reginaandrew.com/"]
        self.siteID = 6
        self.login_url = ""
        self.headers_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3"]

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
            # get all category
            _all_category = response.xpath('//ul[@class="header-menu-level2 has-image"]/li/a/@href').extract()
            if len(_all_category) <= 0:
                pass
            else:
                for _category_link in _all_category:
                    abs_category_link = response.urljoin(_category_link)
                    yield Request(url=abs_category_link, callback=self.parse_deep,
                                  headers={'User-Agent': self.header})

    def parse_after_login(self, response):
        self._login = False
        print("logged in")
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': self.header})

    def parse_deep(self, response):
        # get the item int
        _item_amount = response.xpath('//header[@class="facets-facet-browse-header"]/h3/text()').extract_first()
        _item_amount_int = int(re.sub(r'([p|P]roduct?s)', '', _item_amount).strip())
        _total_times_to_call_ajax = []
        for i in range(0, _item_amount_int, 12):
            _total_times_to_call_ajax.append(i)
        # Ajax Call Build up
        for j in range(1, len(_total_times_to_call_ajax) + 1):
            make_url_with_ajax = response.url + f"?page={j}"
            yield Request(url=make_url_with_ajax, callback=self.parse_item_links,
                          headers={'User-Agent': self.header})

    def parse_item_links(self, response):
        print(f"grabbing link {response.url}")
        _all_item_links = response.xpath('//div[@itemprop="itemListElement"]/meta[@itemprop="url"]/@content').extract()
        for _item_link in _all_item_links:
            abs_item_link = response.urljoin(_item_link)
            yield Request(url=abs_item_link, callback=self.parse_item,
                          headers={'User-Agent': self.header})

    def parse_item(self, response):
        # grab actual data here
        if not self._take_price:
            _productItem = ProductItems()
            item_name = response.xpath('//h1[@class="item-details-content-header-title"]/text()').extract_first()
            if not item_name:
                item_name = ""
            sku = response.xpath('//span[@itemprop="sku"]/text()').extract_first()
            if not sku:
                sku = ""
            else:
                sku = sku.strip()
            item_description = response.xpath('//div[@class="item-details-description"]/text()').extract_first()
            if not item_description:
                item_description = ""
            else:
                item_description = item_description.strip()

            _height = response.xpath(
                '//div[@class="item-details-content"]/div[contains(text(), "Height: ")]/text()').extract_first()
            if not _height:
                _height = ""
            else:
                _height = _height.strip()
            _width = response.xpath(
                '//div[@class="item-details-content"]/div[contains(text(), "Width: ")]/text()').extract_first()
            if not _width:
                _width = ""
            else:
                _width = _width.strip()
            _depth = response.xpath(
                '//div[@class="item-details-content"]/div[contains(text(), "Depth: ")]/text()').extract_first()
            if not _depth:
                _depth = ""
            else:
                _depth = _depth.strip()
            dimension = f"{_height} x {_width} x {_depth}"

            _photos = response.xpath('//ul[@class="bxslider"]/li/noscript/img/@src').extract()
            photos = []
            if len(_photos) <= 0:
                photos = []
            else:
                for p in _photos:
                    h, sep1, t = p.partition('?')
                    if h not in photos:
                        photos.append(h)

            _category = response.xpath('//ul[@itemprop="breadcrumb"]/li/a/text()').extract()
            _category.pop(0)
            _cat = '/'.join(_category).strip()

            _productItem['SiteId'] = self.siteID
            _productItem['SKU'] = sku
            _productItem['ItemName'] = item_name
            _productItem['Category'] = _cat
            _productItem['URL'] = response.url
            _productItem['ItemDescription'] = item_description
            _productItem['Dimension'] = dimension
            _productItem['Photo'] = photos
            yield _productItem
        else:
            _priceItem = PriceItems()
            _sku = response.xpath('//span[@itemprop="sku"]/text()').extract_first()
            if not _sku:
                _sku = ""
            else:
                _sku = _sku.strip()

            _net = ""
            if not _net:
                _net = ""

            _priceItem['SiteId'] = self.siteID
            _priceItem["SKU"] = _sku
            _priceItem["MSRP"] = ""
            _priceItem["NET"] = _net
            _priceItem["AccountId"] = self.customer_id
            yield _priceItem
