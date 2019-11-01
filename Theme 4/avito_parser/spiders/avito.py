# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avito_parser.items import AvitoParserItem

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/kvartiry?cd=1']

    def parse(self, response: HtmlResponse):
        next_link = response.xpath('//a[contains(@class, "js-pagination-next")]/@href').extract_first()
        yield response.follow(next_link, callback=self.parse)

        item = AvitoParserItem()
        apartments_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for itm in apartments_links:
            item['url'] = itm
            yield response.follow(itm, callback=self.parse_apartment_page, meta={'item': item})
        

    def parse_apartment_page(self, response: HtmlResponse):
        item = response.meta['item']
        item['name'] = response.xpath('//span[@class="title-info-title-text"]/text()').extract_first()
        item['cost'] = int(response.xpath('//span[@class="js-item-price"]/@content').extract_first())
        item['images'] = response.xpath('//div[contains(@class, "gallery-img-wrapper")]/div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        item['autor_url'] = response.xpath('//div[contains(@class, "seller-info-name")]/a/@href').extract_first()
        item['autor_name'] = response.xpath('//div[contains(@class, "seller-info-name")]/a/text()').extract_first()
        yield item