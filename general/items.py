# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItems(scrapy.Item):
    # define the fields for products
    SiteId = scrapy.Field()
    SKU = scrapy.Field()
    ItemName = scrapy.Field()
    Category = scrapy.Field()
    URL = scrapy.Field()
    ItemDescription = scrapy.Field()
    Dimension = scrapy.Field()
    Photos = scrapy.Field()


class PriceItems(scrapy.Item):
    # define the fields for price
    SKU = scrapy.Field()
    MSRP = scrapy.Field()
    NET = scrapy.Field()
    CUSTOMERID = scrapy.Field()
