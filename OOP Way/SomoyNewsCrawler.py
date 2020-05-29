from NewsCrawler import NewsCrawler
import requests
import bs4
from datetime import datetime

class SomoyNewsCrawler(NewsCrawler):
    def __init__(self):
        super().__init__(source_id = 3, source_name= 'SomoyNews', base_url = 'https://www.somoynews.tv/')
        
    def fetch_article(self, iteam_url):
        c=0
        try:
            source_code = requests.get(iteam_url)
        except:
            return None
        pain_text = source_code.text
        soup = bs4.BeautifulSoup(pain_text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()    
        for item_name in soup.findAll('h1', {'class': 'title'}):
            headLine=item_name.text
            c+=1
        itemBody=""    
        for item_name in soup.findAll('div', {'class': 'spc_d'}):
            itemBody=item_name.text
            c+=1

        for item_name in soup.findAll('div', {'class': 'news-info'}):
            data = item_name.text.split(" ")
            date = data[1].split(",")
            itemDate=date[0]
        #cpy_sheet.write(count, 1, item_name.text)
        try:
            if(c==2):
                return {
                    'timestamp'    : datetime.now(),
                    'article_url'  : iteam_url,
                    'article_title': headLine,
                    'article_body' : itemBody,
                    'date_published' : itemDate
                }
            return None
        except:
            return None
    def fetch_all_articles(self, base_url = None):
        co=0
        #print("SN-start")
        if base_url is None:
            base_url = self.base_url
        articles = []
        source_code = requests.get(base_url)
        plain_text = source_code.text
        soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
        for link in soup2.findAll('a'):
        #for link in soup2.findAll('a', {'class': 'spark'}):
            #print(link.get('href'))
            try:
                st=link.get('href').split(":")
                if(st[0]=="https" or st[0]=="http"):
                    href=link.get('href')
                else:
                    href = "https://www.somoynews.tv"+link.get('href')
                if(href.find("https://www.somoynews.tv/pages/details") !=-1 ):
                    article = self.fetch_article(href)
                    if article is not None:
                        articles.append(article)
                        #print(co+1)
                        co=co+1;
                        #print('Somoy News...')
                        #print(article['article_title'])
                        #print(article['article_body'])
            except:
                print("Problem while extracting from SomoyNews...")
            if(co==100):
                break
        #print("DA-end")
        return {
            'timestamp'    : datetime.now(),
            'base_url'     : base_url,
            'article_count': len(articles),
            'articles'     : articles
        }

