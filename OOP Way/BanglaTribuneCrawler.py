#!/usr/bin/env python
# coding: utf-8

# In[2]:


from NewsCrawler import NewsCrawler
import requests
import bs4
from datetime import datetime

class BanglaTribuneCrawler(NewsCrawler):
    def __init__(self):
        super().__init__(source_id = 6, source_name= 'BanglaTribune', base_url = 'https://www.banglatribune.com/')
        
    def fetch_article(self, item_url):
        c=0
        try:
            source_code = requests.get(item_url)
        except:
            return None
        pain_text = source_code.text
        soup2 = bs4.BeautifulSoup(pain_text, 'html.parser')
        for script in soup2(["script", "style"]):
            script.decompose()    
        for soup in soup2.findAll('div', {'class': 'detail_article'}):
            for item_name in soup.findAll('span', {'class': 'title'}):
                headLine=item_name.text
                c+=1
            itemBody=""    
            for item_name in soup.findAll('div', {'itemprop': 'articleBody'}):
                itemBody=item_name.text
                c+=1
                #print(itemBody)
            for item_name in soup.findAll('span', {'class': 'time'}):
                data = item_name.text.split(",")
                #date = data[1].split(",")
                itemDate=""
                itemDate=data[1]+data[2]
                #print(val3)
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
        #print("BT-start")
        if base_url is None:
            base_url = self.base_url
        articles = []
        source_code = requests.get(base_url)
        plain_text = source_code.text
        soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
        for li in soup2.findAll('h2', {'class': 'title_holder'}):
            for link in li.findAll('a'):
                try:
                    st=link.get('href').split(":")
                    if(st[0]=="https" or st[0]=="http"):
                        href=link.get('href')
                    else:
                        href = "https://www.banglatribune.com"+link.get('href')
                    #print(href)
                    article = self.fetch_article(href)
                    if article is not None:
                        articles.append(article)
                        #print(co+1)
                        co=co+1;
                        #print(self.source_name)
                        #print('Bangla Tribune...')
                        #print(article['article_title'])
                except:
                    print("Problem while extracting from BanglaTribune...")
            if(co>70):
                break
        #print("BT-end")
        return {
            'timestamp'    : datetime.now(),
            'base_url'     : base_url,
            'article_count': len(articles),
            'articles'     : articles
        }
#crawler = BanglaTribuneCrawler()
#ans = crawler.fetch_all_articles()
#print(ans)


# In[ ]:




