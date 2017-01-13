# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

import scrapy

from chinese_shops.items import ChineseShopsItem


def parse_numbers(string):
    return re.findall(r'\d+', string)[0]

start_url = (
    'https://search.jd.com/s_new.php?keyword=qnap&enc=utf-8&qrst=1&rt=1&stop=1&vt=2'
    '&bs=1&wq=qnap&ev=exbrand_%E5%A8%81%E8%81%94%E9%80%9A%EF%BC%88QNAP%EF%BC%89%40'
    '&page={}&s=31&scrolling=y'
)


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com", "p.3.cn",  "c0.3.cn"]
    start_urls = ['http://jd.com/']

    def start_requests(self):
        for page in range(1, 14):
            yield scrapy.Request(url=start_url.format(page),
                                 callback=self.parse_list)

    def parse_list(self, response):
        for url in response.xpath('//li[@class="gl-item"]/div/div[@class="p-img"]/a/@href').extract():
            yield scrapy.Request(url='https:' + url,
                                 callback=self.parse_item)

    def parse_item(self, response):
        item = ChineseShopsItem()
        item['URL'] = response.url
        item['Name'] = response.xpath(
            '//div[@class="sku-name"]/text()').extract()
        item['Brand'] = response.xpath(
            '//ul[@id="parameter-brand"]/li[1]/a[1]/text()').extract_first()
        item_id = parse_numbers(response.xpath('//ul[@id="parameter2"]/li[2]/text()').extract_first()
                                or
                                response.xpath(
                                    '//ul[@class="parameter2 p-parameter-list"]/li[2]/text()').extract_first()
                                )

        item['MPN'] = item_id

        url = 'https://p.3.cn/prices/get?&skuid=J_{}'.format(item_id)

        cat_ids = re.findall(
            "cat:\[(.*)\]", response.body, re.MULTILINE)[0][1:-1].split('|')
        yield scrapy.Request(url=url,
                             meta={'item': item,
                                   'cat_ids': cat_ids},
                             callback=self.get_price)

    def get_price(self, response):
        item = response.meta['item']
        item['Price'] = json.loads(response.body)[0]['p']
        url = 'https://c0.3.cn/stock?skuId={}&cat={}&area=1_72_2799_0'.format(
            item['MPN'], ','.join(response.meta['cat_ids']))
        yield scrapy.Request(url=url,
                             meta={'item': item},
                             callback=self.get_stock_state)

    def get_stock_state(self, response):
        item = response.meta['item']
        data = json.loads(response.body_as_unicode())
        item['Stock'] = '0' if data['stock']['StockState'] == 33 else ''
        yield item
