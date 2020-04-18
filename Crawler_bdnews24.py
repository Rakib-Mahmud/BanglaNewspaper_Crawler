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
create_table=False
if create_table:
    mycursor.execute("CREATE TABLE IF NOT EXISTS `crawler_bdnews24` (Date VARCHAR(30),Headline VARCHAR(200) PRIMARY KEY,Content TEXT)")
#Comments are writen as a descriptor of the underneath line

def get_single_item_data(item_url):
    global count
    c=0
    try:
        source_code = requests.get(item_url)
    except:
        return
    pain_text = source_code.text
    soup = bs4.BeautifulSoup(pain_text, 'html.parser')
    count+=1
    print(count)
    for item_name in soup.findAll('h1', {'class': 'print-only'}):
        val1=item_name.text
        print(val1)
        c+=1
    val2=""    
    for item_name in soup.findAll('div', {'class': 'custombody print-only'}):
        for content in item_name.findAll('p'):
            val2+=content.text
            print(val2)
        
    for item_name in soup.findAll('div', {'id': 'esi_date'}):
        data = item_name.text.split(",")
        val3=data[0]
        print(val3)
#        cpy_sheet.write(count, 1, item_name.text)
    try:
        if(c!=0):
            sql="INSERT INTO crawler_bdnews24 (Date,Headline,Content) VALUES (%s,%s,%s)"
            print(val1)   
            val=(val3,val1,val2)
            mycursor.execute(sql,val)
    except:
        return
#tt defines the number of times crawler updates
tt=0
#while True:
url = 'https://bangla.bdnews24.com/' 
source_code = requests.get(url)
print(12)
plain_text = source_code.text
soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
for link in soup2.findAll('a'): 
    href = link.get('href')
    st=href.split(":")
    #print(st)
    #function to get to the page containing headline along with the news
    if(st[0]=="https"):
        #print(href)
        get_single_item_data(href)
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
    
