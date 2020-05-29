#!/usr/bin/env python
# coding: utf-8

# In[2]:


from NewsCrawler import NewsCrawler
import requests
import bs4
from datetime import datetime

class BdNewsCrawler(NewsCrawler):
    def __init__(self):
        super().__init__(source_id = 5, source_name= 'BdNews', base_url = 'https://bangla.bdnews24.com/')
        
    def fetch_article(self, item_url):
        c=0
        try:
            source_code = requests.get(item_url)
        except:
            return None
        pain_text = source_code.text
        soup = bs4.BeautifulSoup(pain_text, 'html.parser')
        for item_name in soup.findAll('h1', {'class': 'print-only'}):
            headLine=item_name.text
            c+=1
        #print(headLine)
        itemBody=""    
        for item_name in soup.findAll('div', {'class': 'custombody print-only'}):
            for content in item_name.findAll('p'):
                itemBody+=content.text
                #print(val2)

        for item_name in soup.findAll('div', {'id': 'esi_date'}):
            data = item_name.text.split(",")
            itemDate=data[0]
            #print(val3)
        try:
            if(c!=0):
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
        #print("BN-start")
        if base_url is None:
            base_url = self.base_url
        articles = []
        source_code = requests.get(base_url)
        plain_text = source_code.text
        soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
        ext=0
        for link in soup2.findAll('a'):
            #print(link)
            ext+=1
            try:
                href = link.get('href')
                st=href.split(":")
                if(st[0]=="https"):
                    article = self.fetch_article(href)
                    if article is not None:
                        articles.append(article)
                        #print(co+1)
                        co=co+1;
                        #print('BDNews24...')
                        #print(self.source_name)
                        #print(article['article_title'])
            except:
                    print("Problem while extracting from BDNews24...")
            if(co>70):
                break
        #print("BN-end")
        return {
            'timestamp'    : datetime.now(),
            'base_url'     : base_url,
            'article_count': len(articles),
            'articles'     : articles
        }
                
#crawler = BdNewsCrawler()
#ans = crawler.fetch_all_articles()
#print(ans)


# In[ ]:




