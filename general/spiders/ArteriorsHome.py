# -*- coding: utf-8 -*-
import re
from scrapy import Request, FormRequest
from scrapy import Spider
from loginform import fill_login_form


class ArteriorshomeSpider(Spider):
    name = 'ArteriorsHome'
    allowed_domains = ['www.arteriorshome.com']

    def __init__(self, **kwargs):
        super(ArteriorshomeSpider, self).__init__(**kwargs)
        self._username = kwargs.get("_username")
        self._password = kwargs.get("_password")
        self._login = kwargs.get("_signin")
        self._take_price = kwargs.get("_signin")
        self.start_urls = ["https://www.arteriorshome.com/shop"]
        self.siteID = 3
        self.login_url = "https://www.arteriorshome.com/customer/account/login/"
        self.headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3"
        self.customer_id = kwargs.get("_custometid")

        if self._login == "True":
            self._login = True
            self._take_price = self._login
        else:
            self._login = False
            self._take_price = self._login

    def start_requests(self):
        if self._login:
            yield Request(self.login_url, headers={'User-Agent': self.headers})
        else:
            for url in self.start_urls:
                yield Request(url, headers={'User-Agent': self.headers})

    def parse(self, response):
        if self._login:
            # fill login form
            data, url, method = fill_login_form(response.url, response.body,
                                                self._username, self._password)

            # send a request with our login data
            yield FormRequest(url, formdata=dict(data),
                              method=method, callback=self.parse_after_login, headers={'User-Agent': self.headers})
        else:
            _all_category = response.xpath('//ul[@class="category-list"]/li/a/@href').extract()
            if len(_all_category) <= 0:
                yield {
                    "Changed": f"Changed Category '_all_category' Xpath at {response.url}"
                }
            else:
                for _category_link in _all_category:
                    if _category_link == "https://www.arteriorshome.com/shop/on-sale":
                        yield Request(url=_category_link, callback=self.parse_item_links,
                                      headers={'User-Agent': self.headers})
                    else:
                        yield Request(url=_category_link, callback=self.parse_subcategory,
                                    headers={'User-Agent': self.headers})

    def parse_after_login(self, response):
        self._login = False
        print(f"logged in")
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': self.headers})

    def parse_subcategory(self, response):
        print(f"parsing sub category {response.url}")
        # get sub categories link
        _all_sub_category = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()
        if len(_all_sub_category) <= 0:
            yield {
                "Changed": f"Changed Detected, check '_all_sub_category' Xpath for {response.url}"
            }
        else:
            for _sub_category in _all_sub_category:
                yield Request(url=_sub_category, callback=self.parse_deep, headers={'User-Agent': self.headers})

    def parse_deep(self, response):
        _all = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()
        if _all:
            print(f"Found more sub category {response.url}")
            for a in _all:
                yield Request(url=a, callback=self.parse_deep, headers={'User-Agent': self.headers})
        else:
            # load all items and get links
            _item_amount = response.xpath('//div[@class="pager"]/p/text()').extract_first()
            if not _item_amount:
                _item_amount = response.xpath('//div[@class="pager"]/p/strong/text()').extract_first()
            if not _item_amount == '\n':
                _item_amount_int = int(re.sub(r'([i|I]tem\(s\)|[i|I]tems?)', '', _item_amount).strip())
                _total_length = []
                for i in range(0, _item_amount_int, 20):
                    _total_length.append(i)
                # Ajax Call Build up
                for j in range(0, len(_total_length)+1):
                    make_url_with_ajax = response.url + f"?p={j}&is_ajax=1"
                    yield Request(url=make_url_with_ajax, callback=self.parse_item_links, headers={'User-Agent': self.headers})
            else:
                _item_amount = response.xpath('//div[@class="pager"]/p/strong/text()').extract_first()
                _item_amount_int = int(re.sub(r'([i|I]tem\(s\)|[i|I]tems?)', '', _item_amount).strip())
                _total_length = []
                for i in range(0, _item_amount_int, 20):
                    _total_length.append(i)

                for j in range(0, len(_total_length) + 1):
                    make_url_with_ajax = response.url + f"?p={j}&is_ajax=1"
                    yield Request(url=make_url_with_ajax, callback=self.parse_item_links, headers={'User-Agent': self.headers})

    def parse_item_links(self, response):
        # grab item link
        print(f"grabbing {response.url}")
        item_links = response.xpath('//li[@class="item"]/a/@href').extract()
        _all_cat = response.xpath('//ul[@class="breadcrumb"]/li')
        _cat1 = _all_cat[-2].xpath('.//a/text()').extract_first()
        if not _cat1:
            _cat1 = f"Changed Second Category Xpath at {response.url}"
        _cat2 = _all_cat[-1].xpath('.//strong/text()').extract_first()
        if not _cat2:
            _cat2 = f"Changed Last Category at Xpath at {response.url}"
        _category = _cat1 + "\\" + _cat2
        for item in item_links:
            yield Request(url=item, callback=self.parse_item, headers={'User-Agent': self.headers}, meta={'cat': _category})

    def parse_item(self, response):
        print(f"grabbing item {response.url}")
        _category = response.meta['cat']
        # grab actual data here
        if not self._take_price:
            item_name = response.xpath('//div[@class="product-name"]/h1/text()').extract_first()
            if not item_name:
                item_name = f"Item Name Xpath Changed at {response.url}"
            sku = response.xpath('//span[@id="spansku"]/text()').extract_first()
            if not sku:
                sku = f"SKU Xpath Changed at {response.url}"
            item_description = response.xpath('//div[@id="description"]/text()').extract_first()
            if not item_description:
                item_description = f"Item Description Xpath Changed at {response.url}"
                # elif field['fieldName'] == "Dimension":
            d = response.xpath('//li[@id="dimensions"]/span[@class="data"]/span[@class="product-diamen"]/text()').extract()
            if len(d) <= 0:
                dimension = f"Dimension Xpath Changed at {response.url}"
            else:
                dimension = ', '.join(d)
                # elif field['fieldName'] == "Photos":
            photos = response.xpath('//li[@class="item"]/a/img/@src').extract()
            if len(photos) <= 0:
                photos = f"Photos Xpath Changed {response.url}"

            site_id = self.siteID

            yield {
                "SiteId": site_id,
                "Sku": sku,
                "ItemName": item_name,
                "Category": _category,
                "Url": response.url,
                "ItemDescription": item_description,
                "Dimension": dimension,
                "Photo": photos
            }
        else:
            sku = response.xpath('//span[@id="spansku"]/text()').extract_first()
            if not sku:
                sku = f"SKU Xpath Changed at {response.url}"
            _msrp = response.xpath('//p[@class="sugested-price "]/span[@class="price"]/text()').extract_first()
            if not _msrp:
                _msrp = f"MSRP Xpath Changed at {response.url}"
            _net = response.xpath('//p[@class="normal-price"]/span[@class="price"]/text()').extract_first()
            if not _net:
                _net = f"NET Xpath Changed at {response.url}"

            yield {
                "SKU": sku,
                "MSRP": _msrp,
                "Net": _net,
                "CustomerID": self.customer_id
            }
