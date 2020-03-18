from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from zillow.spiders.zillowhouses import ZillowhousesSpider
from zillow import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    town_link_list = ['homes/New-Orleans,-LA_rb']
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(ZillowhousesSpider, town_link_list)
    process.start()