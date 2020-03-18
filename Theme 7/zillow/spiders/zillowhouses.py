# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from urllib.parse import urljoin
from zillow.items import ZillowItem
import time

class ZillowhousesSpider(scrapy.Spider):
    name = 'zillowhouses'
    allowed_domains = ['zillow.com', 'photos.zillowstatic.com', 'zillowstatic.com']
    start_urls = ['http://zillow.com/']
    browser = webdriver.Chrome()

    def __init__(self, town_link_list):
        self.town_link_list = town_link_list

    def parse(self, response: HtmlResponse):
        for town in self.town_link_list:
            yield response.follow(urljoin(self.start_urls[0], town), callback=self.parse_town)
        
    def parse_town(self, response: HtmlResponse):
        pagination = response.xpath('//div[@class="search-pagination"]/ol[@class="zsg-pagination"]/\
                                    li[@class="zsg-pagination-next"]/a/@href').extract_first()
        yield response.follow(urljoin(self.start_urls[0], pagination), callback=self.parse_town)
        houses_link_list = response.xpath('//div[@id="search-page-list-container"]//\
                                            ul[contains(@class, "photo-cards")]/li/article[contains(@class, "list-card")]\
                                            /a[contains(@class, "list-card-info")]/@href').extract()
        for house in houses_link_list:
            yield response.follow(house, callback=self.parse_house)
        
    def parse_house(self, response: HtmlResponse):
        item = ZillowItem()
        self.browser.get(response.url)
        media = self.browser.find_element_by_xpath('//ul[@class="media-stream"]')
        photo_len = len(self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
        while True:
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            tmp_len = len(self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
            if photo_len == tmp_len:
                break
            photo_len = len(self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
        
        item['photos'] = self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]').get_attribute('srcset')
        item['title'] = response.xpath('//h1[@class="ds-address-container"]/span/text()').extract()
        item['description'] = response.xpath('//div[@class="ds-overview-section"]/div[contains(@class, "Text-sc-1vuq29o-0")]/text()').extract_first()
        item['params'] = response.xpath('//ul[@class="ds-home-fact-list"]/li[@class="ds-home-fact-list-item"]/span/text()').extract()
        yield item