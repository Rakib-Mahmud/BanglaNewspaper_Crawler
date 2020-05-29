import sys, os
from datetime import datetime
import time
# import mysql.connector

class PerpetualNewsCrawler:
    def __init__(self, crawlers, crawl_interval):
        self.crawlers = crawlers
        self.crawl_interval = crawl_interval
        self.stop_signalled = False
        self.CrawlerUtils = None

    def save_articles(self, articles, source_info):
        '''
        Implement codes for saving articles in DB
        '''
        if self.CrawlerUtils == None: return
        if source_info is not None and articles is not None:
            saved_to_db = 0
            for article in articles['articles']:
                _hash = self.CrawlerUtils.get_article_hash(article)
                if not self.CrawlerUtils.has_article_with_hash(_hash):
                    if self.CrawlerUtils.save_article_to_db(article, _hash, source_info):
                        saved_to_db += 1
            print('Crawled ', articles['article_count'], ' and saved ', saved_to_db, ' articles from ', source_info['source_name'])
  
    def signal_to_stop(self):
        self.stop_signalled = True

    def resume_crawl(self):
        self.stop_signalled = False
        self.crawl()
    
    def crawl(self, persist = True):
        while True:
            for crawler in self.crawlers:                
                articles_info = crawler.fetch_all_articles()
                source_info = crawler.get_source_info()
                self.save_articles(articles_info, source_info)
            if not persist or self.stop_signalled:
                break
            else:
                time.sleep(self.crawl_interval)

