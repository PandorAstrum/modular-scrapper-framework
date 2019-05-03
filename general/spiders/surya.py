# -*- coding: utf-8 -*-
import random
from loginform import fill_login_form
from scrapy import Request, FormRequest, Spider
from general.items import ProductItems, PriceItems


class SuryaSpider(Spider):
    name = 'surya'
    allowed_domains = ['surya.com']
    custom_settings = {
        'COOKIES_ENABLED': True,
        'HTTPCACHE_ENABLED': True,
    }

    def __init__(self, **kwargs):
        super(SuryaSpider, self).__init__(**kwargs)
        self._username = kwargs.get("_username")
        self._password = kwargs.get("_password")
        self._login = kwargs.get("_signin")
        self.customer_id = kwargs.get("_customerid")
        self._take_price = False
        self.start_urls = ["https://surya.com/"]
        self.siteID = 4
        self.login_url = "https://surya.com/Sign-in/"
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
            yield FormRequest.from_response(response=response,
                                      formdata={'UserName': self._username, 'Password': self._password},
                                      clickdata={'id': 'p_lt_ctl06_pageplaceholder_p_lt_ctl01_logonform_Login1_LoginButton'},
                                      callback=self.parse_after_login)
            # data, url, method = fill_login_form(response.url, response.body,
            #                                     self._username, self._password)
            # send a request with our login data
            # yield FormRequest(url, formdata=dict(data),
            #                   method=method, callback=self.parse_after_login,
            #                   headers={'User-Agent': self.header})
        else:
            _all_category = response.xpath('//ul[@id="menuElem"]/li/a/@href').extract()
            if len(_all_category) <= 0:
                pass
            else:
                for _category_link in _all_category:
                    _exclusion = ['/About-Us/', '/FAQ/', '/open-a-trade-account/', '/market-registration', '/SuryaSpaces/']
                    if _category_link not in _exclusion:
                        abs_category_link = response.urljoin(_category_link)
                        yield Request(url=abs_category_link, callback=self.parse_category,
                                        headers={'User-Agent': self.header})

    def parse_after_login(self, response):
        self._login = False
        print("logged in")
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': self.header})

    def parse_category(self, response):
        _all_sub_cat = response.xpath('//li[@class="product-large"]/a/@href').extract()
        if len(_all_sub_cat) <= 0:
            # try to determine page result
            _page_results = response.xpath("//div[@class='PagerResults']/text()").extract_first()
            if _page_results:
                _all_item_links = response.xpath('//span[@class="product-name"]/a/@href').extract()
                for _item_links in _all_item_links:
                    abs_item_link = response.urljoin(_item_links)
                    yield Request(url=abs_item_link, callback=self.parse_item,
                                  headers={'User-Agent': self.header})

                next_page = response.xpath('//a[@class="UnselectedNext"]/@href').extract_first()
                if next_page:
                    abs_next_page = response.urljoin(next_page)
                    yield Request(url=abs_next_page, callback=self.parse_category,
                                  headers={'User-Agent': self.header})
                # pagination items
            else:
                print(f"Found Sub Sub Category inside {response.url}")
                _all_sub_sub = response.xpath('//span[@class="product-name"]/a/@href').extract()
                for _sub_sub in _all_sub_sub:
                    abs_sub_sub = response.urljoin(_sub_sub)
                    yield Request(url=abs_sub_sub, callback=self.parse_category,
                                  headers={'User-Agent': self.header})

        else:
            for _sub_category_link in _all_sub_cat:
                abs_sub_category_link = response.urljoin(_sub_category_link)
                yield Request(url=abs_sub_category_link, callback=self.parse_category,
                                  headers={'User-Agent': self.header})

    def parse_item(self, response):
        # grab actual data here
        if not self._take_price:
            _productItem = ProductItems()
            item_name = response.xpath('//div[@class="tab-info-container"]//h1/text()').extract_first()
            if not item_name:
                item_name = ""
            else:
                item_name = item_name.strip()

            sku = response.xpath('//div[@class="tab-info-container"]//h1/span/text()').extract_first()
            if not sku:
                sku = ""
            else:
                sku = sku.strip()

            item_description = ""
            if not item_description:
                item_description = ""

            dimension = response.xpath('//td[@class="skudim"]/text()').extract_first()
            if dimension:
                dimension = dimension.strip()
            else:
                dimension = ""

            photos = response.xpath('//div[@class="scroller-container skuimage"]//ul[@class="product-image-carousel"]/a/img/@src').extract()
            if len(photos) <= 0:
                photos = []

            _cat = response.xpath('//a[@class="CMSBreadCrumbsLink"]/text()').extract()
            if len(_cat) <= 0:
                _category = ""
            else:
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
            _sku = response.xpath('//div[@class="tab-info-container"]//h1/span/text()').extract_first()
            if not _sku:
                _sku = ""
            else:
                _sku = _sku.strip()

            _msrp = ""

            _net = response.xpath('//table[@class="skusChart"]//td').extract()
            print(_net)
            if not _net:
                _net = ""

            _priceItem['SiteId'] = self.siteID
            _priceItem["SKU"] = _sku
            _priceItem["MSRP"] = _msrp
            _priceItem["NET"] = _net
            _priceItem["AccountId"] = self.customer_id
            yield _priceItem
