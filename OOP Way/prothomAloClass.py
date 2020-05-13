from baseCralerClass import *
# import mysql.connector

class prothomAloCrawler(NewsCrawler):
    def __init__(self):
        super().__init__(source_id = 1, source_name= 'ProthomAlo', base_url = 'https://www.prothomalo.com')
        
    def fetch_article(self, url):
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = bs4.BeautifulSoup(plain_text, 'html.parser')

        header_items =  soup.findAll('h1', {'class': 'title mb10'})
        if len(header_items) > 0:
            article_title = header_items[0].text
        else: return None     

        article_bodies = soup.findAll('div', {'itemprop': 'articleBody'})
        if len(article_bodies) > 0:
            article_body = article_bodies[0].text
        else: return None

        date_published_items = soup.findAll('span', {'itemprop': 'datePublished'})
        if len(date_published_items) > 0:
            date_published = date_published_items[0].text
        else: return None

        return {
            'timestamp'    : datetime.now(),
            'url'          : url,
            'article_date' : date_published,
            'article_title': article_title,
            'article_body' : article_body
        }
        

    def fetch_all_articles(self, base_url = None):
        #print("PA-start")
        co=1
        if base_url is None:
            base_url = self.base_url
        articles = []

        source_code = requests.get(base_url)
        plain_text = source_code.text
        soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
        for link in soup2.findAll('a',{'class':'link_overlay'}):   
            href = base_url + link.get('href')                
            article = self.fetch_article(href)
            if article is not None:
                articles.append(article)
                #print(co)
                co=co+1;
                print('Prothom Alo...')
                print(article['article_title'])
                #print(article['article_body'])
        #print("PA-end")
        return {
            'timestamp'    : datetime.now(),
            'base_url'     : base_url,
            'article_count': len(articles),
            'articles'     : articles
        }