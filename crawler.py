#!/usr/bin/env python
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool

HEADERS={'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

def get_html(url,params=None):
    r= requests.get(url, headers=HEADERS,params=params)
    return r

def get_all_links(html):
    soup=BeautifulSoup(html,'html.parser')
    tds= soup.find_all('tr',class_='cmc-table-row')#,class_='cmc-table__cell')
    links=[]
    for td in tds:
        try:
            a= td.find('a').get('href')
            a='https://coinmarketcap.com'+a
            if a not in links:
                links.append(a)
        except:
            pass
    return links

def get_page_data(html):
    soup=BeautifulSoup(html,'html.parser')
    cName=price=''
    try:
        names=soup.find('h2',class_='sc-1q9q90x-0')
        # print(names.text)
        cName=names.text.strip()
    except:
        name=''
    try:
        prices=soup.find('div',class_='priceValue')
        price=prices.text.strip()
    except:
        price=''
    data={'name':cName,'price':price}
    return data 
def write_csv(data):
    with open('coinmarketcap.csv','a') as f:
        writer=csv.writer(f)
        
        if data['name']!='':
            writer.writerow((data['name'],data['price']))
            print(data['name'],'parsed')
def make_all(url):
    html=get_html(url)
    data=get_page_data(html.text)
    write_csv(data)

def main():
    url='https://coinmarketcap.com/all/views/all/'
    start=datetime.now()

    html=get_html(url)
    if html.status_code==200:
        print(html.status_code)
        all_links=get_all_links(html.text)

        with Pool(62) as p:
            p.map(make_all,all_links)
    end=datetime.now()
    total=end - start
    print(str(total))
        
if __name__=='__main__':
    main()
    