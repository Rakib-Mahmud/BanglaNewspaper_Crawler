from CrawlerUtils           import CrawlerUtils
from ProthomAloCrawler      import ProthomAloCrawler
from JugantorCrawler        import JugantorCrawler
from BanglaTribuneCrawler   import BanglaTribuneCrawler
from DailyStarCrawler       import DailyStarCrawler
from BdNewsCrawler          import BdNewsCrawler
from SomoyNewsCrawler       import SomoyNewsCrawler
from PerpetualNewsCrawler   import PerpetualNewsCrawler


db_settings = {
    'host'              : 'auth-db146.hostinger.com',
    'port'              : 3306,
    'user'              : 'u259099192_pbdnc',
    'password'          : 'cste@pbdnc',
    'database'          : 'u259099192_pbdnc',
    'autocommit'        : True,
    'raise_on_warnings' : False
}

prothom_alo_crawler = ProthomAloCrawler()
dailyStar_crawler = DailyStarCrawler()
somoyNews_crawler = SomoyNewsCrawler()
bdNews_crawler = BdNewsCrawler()
banglaTribune_crawler = BanglaTribuneCrawler()
jugantor_crawler = JugantorCrawler()
crawlers = [jugantor_crawler, prothom_alo_crawler, dailyStar_crawler, bdNews_crawler, banglaTribune_crawler, somoyNews_crawler ]

PerpetualNewsCrawler = PerpetualNewsCrawler(crawlers, 3600)
CrawlerUtils = CrawlerUtils(db_settings)
PerpetualNewsCrawler.CrawlerUtils = CrawlerUtils

# Make persist = True to run crawling indefinitely
PerpetualNewsCrawler.crawl(persist = False)

print(CrawlerUtils.get_articles_count())

# Use following line to drop articles table from db
# CrawlerUtils.start_over()

del crawlers, PerpetualNewsCrawler, CrawlerUtils




