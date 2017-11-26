from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from uf_app.uf_values_scraper.uf_values_scraper.spiders.uf_values_spider import UFValuesSpider


class Command(BaseCommand):
    help = 'Call uf values spider'

    def handle(self, *args, **options):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(UFValuesSpider)
        process.start()
