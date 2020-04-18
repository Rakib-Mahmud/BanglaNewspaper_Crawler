import requests
import bs4
import mysql.connector

mydb=mysql.connector.connect(
        host="192.168.0.102",
        port=3306,
        user="cste2015-16",
        passwd="nstu101",
        database="cste2015-16"
        )
mycursor=mydb.cursor()
count=0
create_table=True
if create_table:
    mycursor.execute("CREATE TABLE IF NOT EXISTS `crawler_banglatribune` (Date VARCHAR(30),Headline VARCHAR(200),Content TEXT,PRIMARY KEY(Date,Headline))COLLATE utf8mb4_unicode_ci")
#Comments are writen as a descriptor of the underneath line

def get_single_item_data(item_url):
    global count
    c=0
    try:
        source_code = requests.get(item_url)
    except:
        return
    pain_text = source_code.text
    soup2 = bs4.BeautifulSoup(pain_text, 'html.parser')
    for script in soup2(["script", "style"]):
        script.decompose()    
    count+=1
    print(count)
    for soup in soup2.findAll('div', {'class': 'detail_article'}):
        for item_name in soup.findAll('span', {'class': 'title'}):
            val1=item_name.text
            c+=1
            #print(val1)
        val2=""    
        for item_name in soup.findAll('div', {'itemprop': 'articleBody'}):
            val2=item_name.text
            c+=1
            #print(val2)
        for item_name in soup.findAll('span', {'class': 'time'}):
            data = item_name.text.split(",")
            #date = data[1].split(",")
            val3=""
            val3=data[1]+data[2]
            #print(val3)
#        cpy_sheet.write(count, 1, item_name.text)
    try:
        if(c==2):
            sql="INSERT INTO crawler_banglatribune (Date,Headline,Content) VALUES (%s,%s,%s)"
            print(val1)   
            val=(val3,val1,val2)
            mycursor.execute(sql,val)
    except:
        return
#tt defines the number of times crawler updates
tt=0
#while True:
url = 'https://www.banglatribune.com/' 
source_code = requests.get(url)
plain_text = source_code.text
soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
for li in soup2.findAll('h2', {'class': 'title_holder'}):
    for link in li.findAll('a'):
        #print(link.get('href'))
        try:
            st=link.get('href').split(":")
            if(st[0]=="https" or st[0]=="http"):
                href=link.get('href')
            else:
                href = "https://www.banglatribune.com"+link.get('href')
            print(href)    
            get_single_item_data(href)
        except:
            print("Problem in extraction...")
        mydb.commit()
# =============================================================================
#     tt=tt+1
#     print(tt)
#     clk=0
#     #clock to update the system after each 3600 seconds or 60 minutes
#     while clk<3600:
#         time.sleep(1)
#         clk=clk+1
# =============================================================================
    
