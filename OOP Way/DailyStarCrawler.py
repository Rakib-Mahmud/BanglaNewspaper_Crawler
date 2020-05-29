#!/usr/bin/env python
# coding: utf-8

# In[1]:


from NewsCrawler import NewsCrawler
import requests
import bs4
from datetime import datetime

class DailyStarCrawler(NewsCrawler):
    def __init__(self):
        super().__init__(source_id = 4, source_name= 'TheDailyStar', base_url = 'https://www.thedailystar.net/bangla/')
        
    def fetch_article(self, item_url):
        #print("fetch_article called")
        c=0
        try:
            source_code = requests.get(item_url)
        except:
            return None
        pain_text = source_code.text
        soup = bs4.BeautifulSoup(pain_text, 'html.parser')
        for item_name in soup.findAll('h1'):
            headLine=item_name.text
            c+=1
        #print(headLine)
        itemBody=""    
        for item_name in soup.findAll('div', {'class': 'field-body view-mode-teaser'}):
            itemBody=item_name.text
            c+=1
        for item_name in soup.findAll('div', {'class': 'small-text'}):
            data = item_name.text.split(",")
            itemDate=data[3]+data[4]
    #        cpy_sheet.write(count, 1, item_name.text)
        try:
            if(c==2):
                return {
                    'timestamp'    : datetime.now(),
                    'article_url'  : item_url,
                    'article_title': headLine,
                    'article_body' : itemBody,
                    'date_published' : itemDate
                }
            return None
        except:
            return None
    def fetch_all_articles(self, base_url = None):
        co=0
       # print("DS-start")
        if base_url is None:
            base_url = self.base_url
        articles = []
        source_code = requests.get(base_url)
        plain_text = source_code.text
        soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
        for link in soup2.findAll('a'):
            #print(link.get('href'))
            try:
                st=link.get('href').split(":")
                if(st[0]=="https" or st[0]=="http"):
                    href=link.get('href')
                else:
                    href = "https://www.thedailystar.net"+link.get('href')
                #print(len(href))
                #print(href)
                if len(href) > 350:
                   # print("befor fetch_article")
                    article = self.fetch_article(href)
                    #print("after ferch_article")
                    if article is not None:
                        articles.append(article)
                        #print(co+1)
                        co=co+1;
                        #print(self.source_name)
                        #print('Daily Star...')
                        #print(article['article_title'])
            except:
                    print("Problem while extracting from DailyStar...")
                    '''
                    return {
                        'timestamp'    : datetime.now(),
                        'base_url'     : base_url,
                        'article_count': len(articles),
                        'articles'     : articles
                    }
                    '''
            if(co>70):
                break
        #print("DS-end")
        return {
            'timestamp'    : datetime.now(),
            'base_url'     : base_url,
            'article_count': len(articles),
            'articles'     : articles
        }
                
#crawler = dailyStarCrawler()
#ans = crawler.fetch_all_articles()
#print(ans)

