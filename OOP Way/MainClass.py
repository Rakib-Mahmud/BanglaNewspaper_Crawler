#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys, os
import pandas as pd
import numpy as np
from numba import jit
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import signal
import timeit
import math
from datetime import datetime
import requests
import time
import bs4

# import mysql.connector
from prothomAloClass import *
from somoyNewsClass import *
from BanglaTribuneClass import *
from BdNewsClass import *
from DailyStarClass import *
from JugantorClass import *

class CrawlerUtils:    
    def save_article_to_db(self, article, hash):
        '''
        Implement
        '''
    def get_article_hash(self, article):
        return hash(article['article_title'] + article['base_url'])

    def has_article_with_hash(self, _hash):
        '''
        '''
        return False

class PerpetualNewsCrawler:
    def __init__(self, crawlers, crawl_interval):
        self.crawlers = crawlers
        self.crawl_interval = crawl_interval
        self.stop_signalled = True

    def save_articles(self, source_info, articles):
        '''
        Implement codes for saving articles in DB
        '''
        for article in articles['articles']:
            _hash = CrawlerUtils.get_article_hash(article)
            if CrawlerUtils.has_article_with_hash(_hash):
                CrawlerUtils.save_article_to_db(article, _hash)

        if source_info is not None and articles is not None:
            print('crawled ', articles['article_count'], ' articles from ', source_info['source_name'])
  
    def signal_to_stop(self):
        self.stop_signalled = True

    def resume_crawl(self):
        self.stop_signalled = False
        self.crawl()
    
    def crawl(self):
        while True:
            for crawler in self.crawlers:
                source_info = crawler.get_source_info()
                articles_info = crawler.fetch_all_articles()
                #print(crawler.base_url)
                #self.save_articles(source_info, articles_info)
            if self.stop_signalled:
                break
            else:
                time.sleep(self.crawl_interval)
        
prothomAlo_crawler = prothomAloCrawler()
dailyStar_crawler = dailyStarCrawler()
somoyNews_crawler = somoyNewsCrawler()
bdNews_crawler = bdNewsCrawler()
banglaTribune_crawler = banglaTribuneCrawler()
jugantor_crawler = jugantorCrawler()
crawlers = [jugantor_crawler, prothomAlo_crawler, dailyStar_crawler, bdNews_crawler, banglaTribune_crawler, somoyNews_crawler ]
#crawlers = [jugantor_crawler]
PerpetualNewsCrawler = PerpetualNewsCrawler(crawlers, 3600)
PerpetualNewsCrawler.crawl()


# PerpetualNewsCrawler.signal_to_stop()


# In[ ]:





# In[ ]:




