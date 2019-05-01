# -*- coding: utf-8 -*-
import re
import random
from scrapy import Request, FormRequest, Spider
from loginform import fill_login_form
from general.items import ProductItems, PriceItems


class CenturyfurnitureSpider(Spider):
    name = 'centuryfurniture'
    allowed_domains = ['www.centuryfurniture.com']

    def __init__(self, **kwargs):
        super(CenturyfurnitureSpider, self).__init__(**kwargs)
        self._username = kwargs.get("_username")
        self._password = kwargs.get("_password")
        self._login = kwargs.get("_signin")
        self.customer_id = kwargs.get("_custometid")
        self._take_price = False
        self.siteID = 1
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
        self.start_urls = ['https://www.curreyandcompany.com/lighting', 'https://www.curreyandcompany.com/Furniture/',
                           'https://www.curreyandcompany.com/Accessories/', 'https://www.curreyandcompany.com/Outdoor/',
                           'https://www.curreyandcompany.com/upholstery/', 'https://www.curreyandcompany.com/Collections-Shop-by-Collection/']

        self.login_url = "https://www.curreyandcompany.com/sign-in/"

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
            _all_sub_category = response.xpath(
                '//ul[@class="nav nav--tree nav--categories nav--depth-1"]/li/a/@href').extract()
            if len(_all_sub_category) <= 0:
                pass
            else:
                for _sub_category_link in _all_sub_category:
                    abs_sub_category_link = response.urljoin(_sub_category_link)
                    yield Request(url=abs_sub_category_link, callback=self.parse_item_links,
                                  headers={'User-Agent': self.header}, meta={'cat': _sub_category_link})
            # _all_category = response.xpath('//ul[@class="nav nav--primary width--layout"]/li/a[@class="nav__link"]/@href').extract()
            # if len(_all_category) <= 0:
            #     pass
            # else:
            #     for _category_link in _all_category:
            #         if _category_link != "/about-us/":
            #             abs_category_link = response.urljoin(_category_link)
            #             yield Request(url=abs_category_link, callback=self.parse_sub_category,
            #                           headers={'User-Agent': self.header})

    def parse_after_login(self, response):
        self._login = False
        print("logged in")
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': self.header})

    def parse_sub_category(self, response):
        _all_sub_category = response.xpath('//ul[@class="nav nav--tree nav--categories nav--depth-1"]/li/a/@href').extract()
        if len(_all_sub_category) <= 0:
            pass
        else:
            for _sub_category_link in _all_sub_category:
                abs_sub_category_link = response.urljoin(_sub_category_link)
                yield Request(url=abs_sub_category_link, callback=self.parse_item_links,
                              headers={'User-Agent': self.header}, meta={'cat': _sub_category_link})

    def parse_item_links(self, response):
        _cat = response.meta['cat']
        # grab item link
        print(f"grabbing {response.url}")
        item_links = response.xpath('//div[@class="grid grid--products"]/article/h5/a/@href').extract()
        for item_link in item_links:
            abs_item_link = response.urljoin(item_link)
            yield Request(url=abs_item_link, callback=self.parse_item, headers={'User-Agent': self.header},
                          meta={"cat": _cat})

        NEXT_PAGE_SELECTOR = 'a.pageLink__next::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            abs_next_page = response.urljoin(next_page)
            yield Request(url=abs_next_page, callback=self.parse_item_links, headers={'User-Agent': self.header},
                          meta={"cat": _cat})

    def parse_item(self, response):
        _category = response.meta['cat']
        print(f"grabbing item {response.url}")
        # grab actual data here
        if not self._take_price:
            _productItem = ProductItems()
            _main = response.xpath('//div[@class="product__right variantMatrix__replacedContent lg-3 md-right"]')

            item_name = _main.xpath('.//h1[@class="product__name"]/text()').extract_first()
            if not item_name:
                item_name = ""
            sku = _main.xpath('.//div[@class="product__property product__sku"]/span[@class="product__propertyValue"]/text()').extract_first()
            if not sku:
                sku = ""
            dimension = _main.xpath('.//h1[@class="product__name"]/following-sibling::span/text()').extract_first()
            if not dimension:
                dimension = ""

            item_description = response.xpath('//div[@class="product__value"]/text()').extract_first()
            if not item_description:
                item_description = ""
            else:
                item_description = item_description.strip()

            photos = []
            photos_src = response.xpath('//div[@class="zoomPanel lg-andUp--inline-block"]/img/@src').extract()
            if len(photos_src) <= 0:
                photos = []
            else:
                for p in photos_src:
                    head, sep, tail = p.partition('?')
                    if head not in photos:
                        photos.append(head)

            _productItem['SiteId'] = self.siteID
            _productItem['SKU'] = sku
            _productItem['ItemName'] = item_name
            _productItem['Category'] = _category
            _productItem['URL'] = response.url
            _productItem['ItemDescription'] = item_description
            _productItem['Dimension'] = dimension
            _productItem['Photo'] = photos
            yield _productItem
        else:
            _priceItem = NormalizePriceItems()
            _main = response.xpath('//div[@class="product__right variantMatrix__replacedContent lg-3 md-right"]')
            _sku = _main.xpath('.//div[@class="product__property product__sku"]/span[@class="product__propertyValue"]/text()').extract_first()
            if not _sku:
                _sku = ""
            _price = _main.xpath('.//span[@class="price__value"]/text()').extract_first()
            print(_price)
            if not _price:
                _price = ""

            _priceItem["SKU"] = _sku
            _priceItem["PRICE"] = _price
            _priceItem["CUSTOMERID"] = self.customer_id
            yield _priceItem
