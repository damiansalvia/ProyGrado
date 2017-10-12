# -*- encoding: utf-8 -*-
'''
Module with a set of web crawlers
 
@author: Nicolás Mechulam, Damián Salvia
'''

from scrapy import Spider
from scrapy.selector import Selector


class SpiderOpinoLetras(Spider):
    name = "OpinoLetras"
    allowed_domains = ["http://www.opinaletras.com/significado/"]
    start_urls = [
        "http://www.opinaletras.com/significado/abel-pintos-aleli",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = {}
            item['text'] = question.xpath(
                '//*[@id="significados"]/div/div[2]/text()').extract()[0]
            item['val'] = question.xpath(
                '//*[@id="resvotemin-2900"]').extract()[0]
            yield item
