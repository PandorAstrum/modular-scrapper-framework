# -*- coding: utf-8 -*-
import random
from loginform import fill_login_form
from scrapy import Request, FormRequest, Spider
from general.items import ProductItems, PriceItems


class NoirfurniturelaSpider(Spider):
    name = 'noirfurniturela'
    allowed_domains = ['noirfurniturela.com']

    def __init__(self, **kwargs):
        super(NoirfurniturelaSpider, self).__init__(**kwargs)
        self._username = kwargs.get("_username")
        self._password = kwargs.get("_password")
        self._login = kwargs.get("_signin")
        self.customer_id = kwargs.get("_customerid")
        self._take_price = False
        self.start_urls = ["https://noirfurniturela.com/categories"]
        self.siteID = 7
        self.login_url = "https://noirfurniturela.com/account/login"
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
            _all_category = response.xpath('//div[@class="item"]/a/@href').extract()
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
        # try to guess if it has inner level of category or get item links
        _items_links = response.xpath('//a[@class="quickview-url"]/@href').extract()
        if len(_items_links) <= 0:
            print(f"Found Inner Sub Category in {response.url}")
            # if len is 0 then again take sub category and call parse_deep
            _all_sub_category = response.xpath('//div[@class="item"]/a/@href').extract()
            for _sub_category in _all_sub_category:
                abs_sub_category_link = response.urljoin(_sub_category)
                yield Request(url=abs_sub_category_link, callback=self.parse_deep,
                              headers={'User-Agent': self.header})
        else:
            # Get total item value
            _item_amount = int(response.xpath('//input[@id="record-count"]/@value').extract_first())

            _total_time_to_call_ajax = []
            for i in range(0, _item_amount, 50):
                _total_time_to_call_ajax.append(i)
            # Ajax Call Build up
            for j in range(1, len(_total_time_to_call_ajax) + 1):
                make_url_with_ajax = response.url + f"?page={j}&sortOn=SortOrder&attributeFilterScope=&direction=asc&q=&filters=UDF16:,UDF17:,UDF18:,UDF19:,UDF20:"
                yield Request(url=make_url_with_ajax, callback=self.parse_item_links,
                              headers={'User-Agent': self.header})

    def parse_item_links(self, response):
        _items_links = response.xpath('//a[@class="quickview-url"]/@href').extract()
        for _link in _items_links:
            abs_link = response.urljoin(_link)
            yield Request(url=abs_link, callback=self.parse_item,
                          headers={'User-Agent': self.header})

    def parse_item(self, response):
        # grab actual data here
        if not self._take_price:
            _productItem = ProductItems()
            item_name = response.xpath('//div[@class="detail"]/h1/text()').extract_first()
            if not item_name:
                item_name = ""
            sku = response.xpath('//p[contains(text(), "ItemID #: ")]/span/text()').extract_first()
            if not sku:
                sku = ""

            item_description = ""

            dimension = response.xpath('//p[contains(text(), "Dimensions(in): ")]/span/text()').extract_first()
            if not dimension:
                dimension = ''

            _main_photo = response.xpath('//div[@id="main-slideshow"]/img/@src').extract_first()
            _other_photo = response.xpath('//div[@id="main-slideshow"]/div/img/@src').extract()
            if len(_other_photo) <= 0:
                h, sep, t = _main_photo.partition('?')
                photos = [h]
            else:
                photos = []
                h1, sep1, t1 = _main_photo.partition('?')
                photos.append(h1)
                for p in _other_photo:
                    h2, sep2, t2 = p.partition('?')
                    if h2 not in photos:
                        photos.append(h2)
            _category = response.xpath(
                '//div[@class="row columns breadcrumbs header"]/div/ul/li/a/text()').extract_first()

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
            _sku = response.xpath('//p[contains(text(), "ItemID #: ")]/span/text()').extract_first()
            if not _sku:
                _sku = ""
            _msrp = ""
            _net = ""

            _priceItem['SiteId'] = self.siteID
            _priceItem["SKU"] = _sku
            _priceItem["MSRP"] = _msrp
            _priceItem["NET"] = _net
            _priceItem["AccountId"] = self.customer_id
            yield _priceItem
