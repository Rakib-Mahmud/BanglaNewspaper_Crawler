import requests
import time
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

#Comments are writen as a descriptor of the underneath line
# =============================================================================
# wb = Workbook()
# sheet1 = wb.add_sheet('Sheet 1') 
# 
# =============================================================================
def get_single_item_data(item_url):
    global count
    count=w_sheet.nrows
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = bs4.BeautifulSoup(plain_text, 'html.parser')
    for item_name in soup.findAll('h1', {'class': 'title mb10'}):
# =============================================================================
#         mycursor.execute("COUNT(*)")
#         ln=mycursor.fetchall()
#         #loop to check 100 recent entries against the present news to avoid redundancy
#         recent = ln-100
#         if recent < 0:
#             recent = 0
#         for i in range(recent,ln):
#             
#           str=w_sheet.cell_value(i,0)  
#           if(item_name.text==str):
#               return
# =============================================================================
        val1=item_name.text
#            cpy_sheet.write(count, 0, item_name.text)
        
    for item_name in soup.findAll('div', {'itemprop': 'articleBody'}):
#        cpy_sheet.write(count, 1, item_name.text)
        val2=item_name.text
    for item_name in soup.findAll('span', {'itemprop': 'datePublished'}):
        data = item_name.text.split(",")
        val3=data[0]
#        cpy_sheet.write(count, 1, item_name.text)
    try:
        sql="INSERT INTO crawler_prothomalo (Date,Headline,Content) VALUES (%s,%s,%s)"
        print(val1)   
        val=(val3,val1,val2)
        mycursor.execute(sql,val)
    except:
        return
#tt defines the number of times crawler updates
tt=0
while True:
    url = 'https://www.prothomalo.com/' 
    source_code = requests.get(url)
    plain_text = source_code.text
    soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
    for link in soup2.findAll('a',{'class':'link_overlay'}):
        #rb=xlrd.open_workbook('Prothom_Alo.xls')
        #Copy file for writing operation
        #wb=copy(rb)
        #sheet for writing operation
        #cpy_sheet=wb.get_sheet(0)
        #sheet for reading operation
        #w_sheet = rb.sheet_by_index(0) 
        href = "https://www.prothomalo.com"+link.get('href')
        #function to get to the page containing headline along with the news
        get_single_item_data(href)
        #save as the same file after each news's extraction
        #wb.save('Prothom_Alo.xls')
        mydb.commit()
    tt=tt+1
    print(tt)
    clk=0
    #clock to update the system after each 3600 seconds or 60 minutes
    while clk<3600:
        time.sleep(1)
        clk=clk+1
    
