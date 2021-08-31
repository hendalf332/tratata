#!/usr/bin/env python
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from random import uniform
import re
import time
import os
import csv
import json
import sys

from utils.decorators import MessageDecorator
from utils.provider import APIProvider
mesgdcrt=MessageDecorator("stat")
users=[]
FILE='vk.com.csv'
FILEJS='vk.com.json'
start_time=time.time()

try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tSome dependencies could not be imported (possibly not installed)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " install all required packages")
    sys.exit(1)

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
def print_logo():
    clr()
    logo="""

                     .    ____/ (  (    )   )  \___
               .         /( (  (  )   _    ))  )   )\        .   .
                       ((     (   )(    )  )   (   )  )   .
            .    .   ((/  ( _(   )   (   _) ) (  () )  )        .   .
                    ( (  ( (_)   ((    (   )  .((_ ) .  )_
     .       .     (_((__(_(__(( ( ( |  ) ) ) )_))__))_)___)   .
         .         ((__)        \\||lll|l||///          \_))       .
                  .       . / (  |(||(|)|||//  \     .    .      .      .
    .       .           .   (   /(/ (  )  ) )\          .     .
        .      .    .     (  . ( ( ( | | ) ) )\   )               .
                           (   /(| / ( )) ) ) )) )    .   .  .       .  .  
    .     .       .  .   (  .  ( ((((_(|)_)))))     )            .
            .  .          (    . ||\(|(|)|/|| . . )        .        .
        .           .   (   .    |(||(||)||||   .    ) .      .         .  
    .      .      .       (     //|/l|||)|\\ \     )      .      .   .
                        (/ / //  /|//||||\\  \ \  \ _)
-------------------------------------------------------------------------

"""
    print(logo)
def check_intr():
    try:
        requests.get("https://github.com")
    except Exception:
        print_logo()
        mesgdcrt.FailureMessage("Poor internet connection detected")
        sys.exit(2)
 
def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer=csv.writer(file,delimiter=';')
        writer.writerow(['Посилання',
            'Ім\'я користувача',
            'Дата Відвідування',
            'День Народження',
            'Групи',
            'Паблики',
            'countList',
            'Данні профілю'])
        for item in items:
            writer.writerow([item['pname'],item['visitDate'],item['birthday'],item['groupList'],item['publics'],item['countList'],item['profiledataList']])

 
def get_html(url,useragent=None,proxy=None):
    r=requests.get(url,headers=useragent,proxies=proxy)
    return r
    
def get_userinfo(html,myurl):
    soup=BeautifulSoup(html,'html.parser')
    user={}
    try:
        pname=soup.find('h1',class_='page_name').text.strip()
        user['url']=myurl
    except:
        pname=''
    user['pname']=pname  
    
    try:
        visitDate=soup.find('div',class_='_profile_online').find('div',class_='profile_online_lv').text.strip()
        print(visitDate)
    except:
        visitDate=''
    user['visitDate']=visitDate    
    try:
        pubs=soup.find_all('div',class_='group_name')
        publics=[]
        # print(pubs)
        for pb in pubs:
            groupname=pb.find('a').text.strip()
            groupLink="https://vk.com"+pb.find('a').get('href')
            print(groupname,groupLink)
            publics.append(groupname+" "+groupLink)
    except:
        publics=[]
    user['publics']=publics
        
    try:
        groups=soup.find('a',href=re.compile('/groups')).find_next('div').find_all('a')
        print('Групи:')
        # print(groups)
        # print(len(groups))
        groupList=[]
        cnt=0
        for group in groups:
            grp="https://vk.com"+group.get('href')+" "+group.text
            groupList.append(grp)
            print(grp)
    except:
        groupList=[]
    user['groupList']=groupList
        
    try:
        counts=soup.find('div',class_='counts_module').find_all('a',class_='page_counter')
        print('Counters: ')
        countList=[]
        for cntItem in counts:
            label=cntItem.find('div',class_='label')
            item=cntItem.find('div',class_='count')
            print(label.text,item.text,end='\n')
            countList.append(label.text.strip()+" " + item.text.strip())
    except:
        countList=''
    user['countList']=countList
    
    try:
        profiledataList=''
        profiledata=soup.find('div',id='page_info_wrap').find_all('div',class_='profile_info_row')
        for item in profiledata:
            print(item.find('div',class_='labeled').text.strip())
            profiledataList+=item.find('div',class_='labeled').text.strip()
    except:
        profiledataList=''
    user['profiledataList']=profiledataList
    res=re.search(r'(\S{3,10} \d{1,2} \d{4}?)',profiledataList)
    if res:
        birthday=res.group(0)
        user['birthday']=birthday
        print(f"[+] День народження:{birthday}")
    else:
        print('[-]Не можемо знайти дня народження')
        user['birthday']=''
        birthday=''
    if pname!='':
        with open(FILE,"a",encoding="utf-8", newline='') as file:
                writer=csv.writer(file,delimiter=';')
                writer.writerow((
                    myurl,
                    pname,
                    visitDate,
                    birthday,
                    groupList,
                    publics,
                    countList,
                    profiledataList
                ))
        print(f"{pname=} {visitDate=}")
        users.append(user)
    print('-'*80)

def main():
    url='https://vk.com/tratata'
    check_intr()
    current_time = time.localtime()
    cur_date=time.strftime('%Y-%m-%d_%H-%M', current_time)
    global FILE
    global FILEJS
    FILEJS="vk.com_"+str(cur_date)+".json"
    FILE="vk.com_"+str(cur_date)+".csv"
    
    useragents=open('user-agents.txt','r').read().split('\n')
    proxies=open('proxylist.txt','r').read().split('\n')
    clr()
    print('Діапазон пошуку id користувачів vkontakte\nНаприклад 325005713:')
    startRg=int(input("Введіть початкове значення:"))
    endRg=int(input("  Введіть кінцеве значення:"))
    with open(FILE,"w",encoding="utf-8", newline='') as file:
        writer=csv.writer(file,delimiter=';')
        writer.writerow(
        (
            'Посилання',
            'Ім\'я користувача',
            'Дата Відвідування',
            'День Народження',
            'Групи',
            'Паблики',
            'countList',
            'Данні профілю'
        )
        )
    for id in range(startRg,endRg):
        url='id'+str(id)
        if url=="":
            os.exit(0)
        url='https://vk.com/'+url
        print(url)
        a = uniform(3,6)
        # print(a)
        sleep(a)
        proxy= {'http':'http://'+choice(proxies)}
        useragent= {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36'}
        try:
            html=get_html(url,useragent,proxy)
            # print(html.text)
            with open("vk.com.html", "w",encoding="utf-8") as file:
                file.write(html.text)
            with open("vk.com.html",encoding="utf-8") as file:
                src = file.read()
            
        except:
            continue
        # print(html.text)
        if html.status_code==200:
            try:
                get_userinfo(html.text,url)
            except KeyboardInterrupt:
                save_file(users,FILE)
                with open(FILEJS,"w",encoding="utf-8") as file:
                    json.dump(users,file,indent=4,ensure_ascii=False)
                os.startfile(FILE)
    with open(FILEJS,"w",encoding="utf-8") as file:
        json.dump(users,file,indent=4,ensure_ascii=False)
    finish_time=time.time()-start_time
    print(f"Затраченое время на работу скрипта: {finish_time}")
                
if __name__=='__main__':
    main()