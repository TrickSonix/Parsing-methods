# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from hh_parser.items import HhParserItem


class HhVacancySpider(scrapy.Spider):
    name = 'hh_vacancy'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Data+science&from=suggest_post']

    def parse(self, response: HtmlResponse):
        paginator = response.css('a.bloko-button.HH-Pager-Controls-Next::attr(href)').extract()
        next_link = paginator[0]
        yield response.follow(next_link, callback=self.parse)

        vacancy_pages = response.css('div.vacancy-serp-item a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for itm in vacancy_pages:
            itm_link = itm.split('?')[0]
            yield response.follow(itm_link, callback=self.parse_vacancy_page)

    #парсер страницы вакансии
    def parse_vacancy_page(self, response: HtmlResponse):
        item = HhParserItem()
        item['title'] = response.css('h1.header').extract()[1]
        item['company'] = {'name': response.css('a.vacancy-company-name span::text').extract_first(),
                   'url_hh': response.css('a.vacancy-company-name::attr(href)').extract_first()}
        item['key_skills'] = response.css('span.Bloko-TagList-Text::text').extract()
        item['salary'] = response.css('p.vacancy-salary::text').extract_first()
        link = item['company']['url_hh']
        yield response.follow(link, callback=self.parse_company_page, meta={'item': item})

    #парсер страницы компании для получения ссылки на сайт компании
    def parse_company_page(self, response: HtmlResponse):
        item = response.meta['item']
        item['company_url'] = response.css('a.company-url::attr(href)').extract_first()
        yield item


