from celery.schedules import crontab
from celery.task import periodic_task
from scrapy.crawler import CrawlerProcess

from uf_app.uf_values_scraper.uf_values_scraper.spiders.uf_values_spider \
    import UFValuesSpider


@periodic_task(
    run_every=(crontab(hour=23, minute=30)),  # Every day at the end of the date (11:00 PM)
    name="update_uf_values",
    ignore_result=True
)
def update_uf_values():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(UFValuesSpider, only_current_year=True)
    process.start()
