import sys, os
import pandas as pd
import numpy as np
from numba import jit
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import signal
import timeit
import math
import cfscrape
import cloudscraper
from datetime import datetime
import requests
import time
import bs4
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask,AnticatpchaException, ImageToTextTask
class NewsCrawler():
    def __init__(self, source_id, source_name, base_url):
        self.source_id = source_id
        self.source_name = source_name
        self.base_url = base_url
    
    def get_source_info(self):
        return {
            'source_id'  : self. source_id,
            'source_name': self. source_name,
            'base_url'   : self.base_url
        }

    def fetch_article(self, url):
        '''
        Must return a dictionary as:
        {
            timestamp      : __ ,
            article_url    : __ ,      
            article_title  : __ ,
            article_body   : __ ,
            date_published : __ ,
            date_modified  : __
        }
        '''
        # raise(NotImplementedError)
    
    def fetch_all_articles(self, base_url = None):
        '''
        Must return a dictionary as:
        {
            timestamp    : __ ,
            base_url     : __ ,
            article_count: __ ,
            articles     : [ {}, {} ]
        }
        '''
        # raise(NotImplementedError)
