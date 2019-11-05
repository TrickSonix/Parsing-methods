from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from instagram.config import INSTA_LOGIN, INSTA_PASSWORD
from instagram import settings
from instagram.spiders.insta import InstaSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    user_list = ['eleth_art']
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaSpider, INSTA_LOGIN, INSTA_PASSWORD, user_list)
    process.start()