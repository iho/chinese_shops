# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChineseShopsItem(scrapy.Item):
    Brand = scrapy.Field()
    MPN = scrapy.Field()
    URL = scrapy.Field()
    Name = scrapy.Field()
    Price = scrapy.Field()
    Stock = scrapy.Field()
