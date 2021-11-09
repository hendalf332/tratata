#!/usr/bin/env python
import requests
from random import choice
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
from random import uniform
import os,sys

proxnum=0
URL="https://free-proxy-list.net/#list"
HEADERS={'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36','accept':'*/*'}
HOST="https://free-proxy-list.net"
def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
def get_details(html,myurl):
    global proxynum
    prox_res=[]
    countrylist=[]
    exclude_countries=[]
    proxcnt=0
    soup=BeautifulSoup(html,'html.parser')
    table=soup.find('div',class_='fpl-list').find('table',class_='table-striped').find('tbody').find_all('tr')
    for rec in enumerate(table):
        try:
            country=rec[1].find('td',class_='hm').text.strip()
            countrylist.append(country)
        except:
            continue
    newcountrylist=list(set(countrylist))
    newcountrylist.sort()
    for rec in enumerate(newcountrylist):
        print(f"{rec[0]}>{rec[1]}")
    exclude_countries=list(map(str, input("Enter number of countries to exclude from search:").lower().split()))
    print(str(exclude_countries))
    input('Press Any Key To View Results...')
    pre="""
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to &amp;amp;amp;amp;amp;amp;quot;tor&amp;amp;amp;amp;amp;amp;quot;
    """
    clr()
    print(pre)
    for prel in enumerate(table):
        try:
            myprox=prel[1].find_all('td')
            for el in myprox:
                elem=el.text.strip()
                res=re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',elem)
                if res:
                    ipaddr=res.group(0)
                res2=re.search(r'^\d+$',elem)
                if res2:
                    port=res2.group(0)
            try:
                elem=prel[1].find('td',class_='hx')
                country=prel[1].find('td',class_='hm').text.strip()
                cntryIdx=newcountrylist.index(country)
                hx=elem.text.strip()
                if hx=='yes' and proxcnt<proxynum and str(cntryIdx) not in exclude_countries:
                    print(f"http\t{ipaddr}\t{port}")
                    proxcnt+=1
            except:
                pass
        except:
            continue
    

def get_html(url,useragent=None,proxy=None):
    print('get-html')
    r=requests.get(url,headers=useragent,proxies=proxy)
    return r

def main():
    global proxynum
    myurl=URL
    try:
        useragent=HEADERS
        html=get_html(myurl,useragent,proxy=None)
    except:
        pass
    if html.status_code==200:
        print('OK')
        proxynum=int(input('Enter number of proxies:'))
        get_details(html.text,myurl)
        print("\n\nСкопіюйте зміст вище в файл /etc/proxychains.conf")
if __name__=='__main__':
	main()
	