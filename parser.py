#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import csv
import os


URL='https://auto.ria.com/newauto/marka-peugeot/'
HEADERS={'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36','accept':'*/*'}
HOST='https://auto.ria.com'
FILE='cars.csv'

def get_html(url,params=None):
    r= requests.get(url, headers=HEADERS,params=params)
    return r
    
def get_pages_count(html):
    soup=BeautifulSoup(html,'html.parser')
    pagination=soup.find_all('span',class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    
def get_content(html):
    soup=BeautifulSoup(html,'html.parser')
    items= soup.find_all('a',class_='proposition_link')
    
    cars=[]
    for item in items:
        uah_price=item.find('span',class_='size16')
        if uah_price:
            uah_price=uah_price.get_text()
        else:
            uah_price='Цену уточняйте!!!'
        cars.append({
            'title':item.find('div',class_='proposition_title').get_text(strip=True),
            'link':HOST+item.get('href'),
            'usd_price':item.find('span',class_='green bold size22').get_text(strip=True).replace(' ',''),
            'grn_price':uah_price.replace(' ',''),
            'misto':item.find('span',class_='item region').get_text(strip=True),
        })
    return cars

def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer=csv.writer(file,delimiter=';')
        writer.writerow(['Марка','Посилання','ЦінаВДОЛ','Ціна в ГРН','Місто'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['usd_price'],item['grn_price'],item['misto']])
    
def parse():
    URL=input('Введіть ПОСИЛАННЯ URL:')
    URL = URL.strip()
    html=get_html(URL)
    if html.status_code==200:
        cars=[]
        pages_count=get_pages_count(html.text)
        #cars=get_content(html.text)
        print(pages_count)
        for page in range(1,pages_count+1):
            print(f'Парсинг сторінки {page} з {pages_count}...')
            html=get_html(URL,params={'page':page})
            cars.extend(get_content(html.text))
        save_file(cars,FILE)
        os.startfile(FILE)
        # print(cars)
        print(f'Отриман {len(cars)} автомобілів!!!')
    else:
        print('Помилка!!!')
    
parse()