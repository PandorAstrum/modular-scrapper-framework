# -*- coding: utf-8 -*-
import re

from scrapy import Request
from scrapy import Spider


class ArteriorshomeSpider(Spider):
    name = 'ArteriorsHome'
    allowed_domains = ['www.arteriorshome.com']

    def __init__(self, **kwargs):
        super(ArteriorshomeSpider, self).__init__(**kwargs)
        self._selected_spider = kwargs.get('_selected_spider')
        self.headers = self._selected_spider['Settings']['User-Agents']
        self.siteID = self._selected_spider['siteID']
        self.start_urls = [self._selected_spider['targetURL']]
        self._take_price = False

    def start_requests(self):
        if self._take_price:
            # self.login_url utilize it
            pass # login here
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': self.headers})

    def parse(self, response):
        # get only categories link
        _all_category = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()
        print(f"Total Length of First Category : {len(_all_category)}")
        for _category_link in _all_category:
            yield Request(url=_category_link, callback=self.parse2, headers={'User-Agent': self.headers})

    def parse2(self, response):
        # get sub categories link
        _all_sub_category = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()

        for _sub_category in _all_sub_category:
            yield Request(url=_sub_category, callback=self.parse3, headers={'User-Agent': self.headers})

    def parse3(self, response):
        all = response.xpath('//ul[@class = "category-list"]/li/a/@href').extract()
        if all:
            for a in all:
                yield Request(url=a, callback=self.parse3, headers={'User-Agent': self.headers})
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
                    print(make_url_with_ajax)
                    yield Request(url=make_url_with_ajax, callback=self.parse4, headers={'User-Agent': self.headers})
            else:
                _item_amount = response.xpath('//div[@class="pager"]/p/strong/text()').extract_first()
                _item_amount_int = int(re.sub(r'([i|I]tem\(s\)|[i|I]tems?)', '', _item_amount).strip())
                _total_length = []
                for i in range(0, _item_amount_int, 20):
                    _total_length.append(i)

                for j in range(0, len(_total_length) + 1):
                    make_url_with_ajax = response.url + f"?p={j}&is_ajax=1"
                    print(make_url_with_ajax)
                    yield Request(url=make_url_with_ajax, callback=self.parse4, headers={'User-Agent': self.headers})

    def parse4(self, response):
        # grab item link
        item_links = response.xpath('//li[@class="item"]/a/@href').extract()
        for item in item_links:
            yield Request(url=item, callback=self.parse_item, headers={'User-Agent': self.headers})

    def parse_item(self, response):
        # grab actual data here
        item_name = response.xpath('//div[@class="product-name"]/h1/text()').extract_first()
        sku = response.xpath('//span[@id="spansku"]/text()').extract_first()
        item_description = response.xpath('//div[@id="description"]/text()').extract_first()
        d = response.xpath('//li[@id="dimensions"]/span[@class="data"]/span[@class="product-diamen"]/text()').extract()
        dimension = ', '.join(d)
        photos = response.xpath('//li[@class="item"]/a/img/@src').extract()
        site_id = self.siteID
        category = ""

        # todo: detect photo length and auto decide to yield
        yield {
            "SiteId": site_id,
            "Sku": sku,
            "ItemName": item_name,
            "Category": category,
            "ItemDescription": item_description,
            "Dimension": dimension,
            "Photo": photos
        }
