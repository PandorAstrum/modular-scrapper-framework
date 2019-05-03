# -*- coding: utf-8 -*-
import random
from loginform import fill_login_form
from scrapy import Request, FormRequest, Spider
from general.items import ProductItems, PriceItems


class AbhomeincSpider(Spider):
    name = 'abhomeinc'
    allowed_domains = ['www.abhomeinc.com']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
	    'COOKIES_ENABLED': False,
	    'HTTPCACHE_ENABLED': True
    }

    def __init__(self, **kwargs):
        super(AbhomeincSpider, self).__init__(**kwargs)
        self._username = kwargs.get("_username")
        self._password = kwargs.get("_password")
        self._login = kwargs.get("_signin")
        self.customer_id = kwargs.get("_customerid")
        self._take_price = False
        self.start_urls = ["https://www.abhomeinc.com/"]
        self.siteID = 0
        self.login_url = "https://www.abhomeinc.com/my-account/"
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
                              headers={'User-Agent': self.header}, dont_filter=True)
        else:
            _all_category = response.xpath('//div[@class="navbar-categories"]/ul[@class="nav navbar-nav nav-centered"]/li/a/@href').extract()
            if len(_all_category) <= 0:
                pass
            else:
                for _category_link in _all_category:
                    _inclusion = ['/flash-sales', '/new-arrivals']
                    if _category_link != "/shop-by-style":
                        if _category_link not in _inclusion:
                            yield Request(url=_category_link, callback=self.parse_category,
                                          headers={'User-Agent': self.header})
                        else:
                            abs_category_link = response.urljoin(_category_link)
                            yield Request(url=abs_category_link, callback=self.parse_item_links,
                                      headers={'User-Agent': self.header})

    def parse_after_login(self, response):
        self._login = False
        print("logged in")
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': self.header})

    def parse_category(self, response):
        _all_sub_cat = response.xpath('//div[@class="category-item-header"]/a/@href').extract()
        if len(_all_sub_cat) <= 0:
           pass  #
        else:
            for _sub_cat in _all_sub_cat:
                yield Request(url=_sub_cat, callback=self.parse_item_links,
                              headers={'User-Agent': self.header})

    def parse_item_links(self, response):
        # get all the item link
        _all_item_links = response.xpath('//div[@class="information"]/a/@href').extract()
        if len(_all_item_links) <= 0:
            pass
        else:
            for _item_link in _all_item_links:
                yield Request(url=_item_link, callback=self.parse_item,
                          headers={'User-Agent': self.header})

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page:
            yield Request(url=next_page, callback=self.parse_item_links,
                          headers={'User-Agent': self.header})

    def parse_item(self, response):
        # grab actual data here
        if not self._take_price:

            _productItem = ProductItems()

            item_name = response.xpath('//h1/strong/text()').extract_first()
            if not item_name:
                item_name = ""
            else:
                item_name = item_name.strip()

            sku = response.xpath('//span[@itemprop="sku"]/text()').extract_first()
            if not sku:
                sku = ""
            else:
                sku = sku.strip()

            _d = response.xpath('//div[@class="product-description"]/text()').extract()
            _d2 = []
            for d in _d:
                if "Measurement" in d:
                    dimension = d.strip()
                else:
                    dimension = ""
                    _d2.append(d.strip())

            item_description = " ".join(_d2)

            photos = response.xpath('//div[@class="product-gallery-item img-wrapper-1"]//img/@src').extract()
            if len(photos) <= 0:
                photos = []

            _cat = response.xpath('//ol[@class="breadcrumb"]/li/a/text()').extract()
            if len(_cat) <= 0:
                _category = ""
            else:
                _cat.pop(0)
                _cat.pop(-1)
                _category = '/'.join(_cat)

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
            _priceItem = PriceItems()
            _sku = response.xpath('//span[@itemprop="sku"]/text()').extract_first()
            if not _sku:
                _sku = ""
            else:
                _sku = _sku.strip()

            _msrp = ""

            _net = response.xpath('//meta[@itemprop="price"]/@content').extract_first()
            _cur = response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract_first()
            if not _net:
                _net = ""
            else:
                _net = f"{_cur} {_net}"

            _priceItem['SiteId'] = self.siteID
            _priceItem["SKU"] = _sku
            _priceItem["MSRP"] = _msrp
            _priceItem["NET"] = _net
            _priceItem["AccountId"] = self.customer_id
            yield _priceItem

