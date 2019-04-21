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
        self._selected_spider = kwargs.get('_selected_spider')
        self.headers = self._selected_spider['Settings']['User-Agents']
        self._login_url = self._selected_spider['loginURL']
        self._default_username = self._selected_spider['username']
        self._default_password = self._selected_spider['password']
        self.siteID = self._selected_spider['siteID']
        self.start_urls = [self._selected_spider['targetURL']]
        self._take_price = self._selected_spider['login']
        self._login = self._selected_spider['login']

    def start_requests(self):
        if self._take_price:
            yield Request(self._login_url, headers={'User-Agent': self.headers})
        else:
            for url in self.start_urls:
                yield Request(url, headers={'User-Agent': self.headers})

    def parse(self, response):
        if self._take_price:
            # do login
            # got the login page, let's fill the login form...
            data, url, method = fill_login_form(response.url, response.body,
                                                self._default_username, self._default_password)

            # ... and send a request with our login data
            yield FormRequest(url, formdata=dict(data),
                              method=method, callback=self.parse_after_login, headers={'User-Agent': self.headers})
        else:
            _all_category = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()
            print(f"Total Length of First Category : {len(_all_category)}")
            for _category_link in _all_category:
                yield Request(url=_category_link, callback=self.parse_subcategory, headers={'User-Agent': self.headers})

    def parse_after_login(self, response):
        self._take_price = False
        print(f"login Status : {response.status}")
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': self.headers})

    def parse_subcategory(self, response):
        # get sub categories link
        _all_sub_category = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()

        for _sub_category in _all_sub_category:
            yield Request(url=_sub_category, callback=self.parse_deep, headers={'User-Agent': self.headers})

    def parse_deep(self, response):
        all = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()
        if all:
            for a in all:
                yield Request(url=a, callback=self.parse_deep, headers={'User-Agent': self.headers})
        else:
            # load all items and get links
            _item_amount = response.xpath('//div[@class="pager"]/p/text()').extract_first()
            if not _item_amount == '\n':
                _item_amount_int = int(re.sub(r'([i|I]tem\(s\)|[i|I]tems?)', '', _item_amount).strip())
                _total_length = []
                for i in range(0, _item_amount_int, 20):
                    _total_length.append(i)

                for j in range(0, len(_total_length)+1):
                    make_url_with_ajax = response.url + f"?p={j}&is_ajax=1"
                    # print(f"Grabbing Items from {make_url_with_ajax}")
                    yield Request(url=make_url_with_ajax, callback=self.parse_item_links, headers={'User-Agent': self.headers})
            else:
                _item_amount = response.xpath('//div[@class="pager"]/p/strong/text()').extract_first()
                _item_amount_int = int(re.sub(r'([i|I]tem\(s\)|[i|I]tems?)', '', _item_amount).strip())
                _total_length = []
                for i in range(0, _item_amount_int, 20):
                    _total_length.append(i)

                for j in range(0, len(_total_length) + 1):
                    make_url_with_ajax = response.url + f"?p={j}&is_ajax=1"
                    # print(f"Grabbing Items from {make_url_with_ajax}")
                    yield Request(url=make_url_with_ajax, callback=self.parse_item_links, headers={'User-Agent': self.headers})

    def parse_item_links(self, response):
        # grab item link
        item_links = response.xpath('//li[@class="item"]/a/@href').extract()
        _all_cat = response.xpath('//ul[@class="breadcrumb"]/li')
        _cat1 = _all_cat[-2].xpath('.//a/text()').extract_first()
        _cat2 = _all_cat[-1].xpath('.//strong/text()').extract_first()
        _category = _cat1 + "\\" + _cat2
        for item in item_links:
            yield Request(url=item, callback=self.parse_item, headers={'User-Agent': self.headers}, meta={'cat': _category})

    def parse_item(self, response):
        _category = response.meta['cat']

        # grab actual data here
        if not self._login:
            for field in self._selected_spider["fields"]:
                if field['fieldName'] == "ItemName":
                    item_name = response.xpath(field['Xpath']).extract_first()
                elif field['fieldName'] == "SKU":
                    sku = response.xpath(field['Xpath']).extract_first()
                elif field['fieldName'] == "ItemDescription":
                    item_description = response.xpath(field['Xpath']).extract_first()
                elif field['fieldName'] == "Dimension":
                    d = response.xpath(field['Xpath']).extract()
                    dimension = ', '.join(d)
                elif field['fieldName'] == "Photos":
                    photos = response.xpath(field['Xpath']).extract()
                elif field['fieldName'] == "Category":
                    pass

            site_id = self.siteID

            yield {
                "SiteId": site_id,
                "Sku": sku,
                "ItemName": item_name,
                "Category": _category,
                "ItemDescription": item_description,
                "Dimension": dimension,
                "Photo": photos
            }
        else:
            _msrp = response.xpath('//p[@class="sugested-price"]/span[@class="price"]/text()').extract_first()
            _net = response.xpath('//p[@class="normal-price"]/span[@class="price"]/text()').extract_first()
            for field in self._selected_spider["fields"]:
                if field['fieldName'] == "SKU":
                    sku = response.xpath(field['Xpath']).extract_first()
            #     elif field['fieldName'] == "ItemDescription":
            #         item_description = response.xpath(field['Xpath']).extract_first()
            #     elif field['fieldName'] == "Dimension":
            #         d = response.xpath(field['Xpath']).extract()
            #         dimension = ', '.join(d)
            #     elif field['fieldName'] == "Photos":
            #         photos = response.xpath(field['Xpath']).extract()
            #     elif field['fieldName'] == "Category":
            #         pass

            yield {
                "SKU": sku,
                "MSRP": _msrp,
                "Net": _net
            }
