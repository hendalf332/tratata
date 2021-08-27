#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from random import choice
from time import sleep
import time
import sys, readchar
from random import uniform
import os
import datetime
users=[]

session = requests.Session()
user_url='http://forum.chornobyl.com.ua/memberlist.php?mode=viewprofile&u='
UAG='Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36'
URL='http://forum.chornobyl.com.ua/ucp.php?mode=login'
HEADERS={'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36','accept':'*/*'}
HOST='http://forum.chornobyl.com.ua'
FILE='forum.chornobyl.com.ua.csv'

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

def passprompt(prompt: str, out = sys.stdout) -> str:
    out.write(prompt); out.flush()
    password = ""
    while True:
        ch = str(readchar.readchar(), encoding='UTF-8')
        if ch == '\r':
            break
        elif ch == '\b':
            if len(password)>0:
                out.write('\b \b')
                password = password[0:len(password)-1]
                out.flush()
        else: 
            password += ch
            out.write("*")
            out.flush()
    print('\n')
    return password
    
def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer=csv.writer(file,delimiter=';')
        writer.writerow(['Nick','ДатаРегистрации','ДатаОст.Визита','Кіл.Повідомлень','Контакти','Звідки','Групи','Діяльність','НайбільшАктивний','Інтереси','Посилання','Сайт'])
        for item in items:
            writer.writerow([item['nick'],item['regdate'],item['visitdate'],item['msgnum'],item['contacts'],item['otkuda'],item['groups'],item['activity'],item['active'],item['interests'],item['url'],item['site']])

def get_html(url,params=None):
    r= requests.get(url, headers=HEADERS,params=params)
    return r
def get_request_html(url,params=None):
    r= session.get(url, headers=HEADERS,params=params)
    return r
def login_auth(sid):
    current_time = time.localtime()
    cur_date=time.strftime('%Y-%m-%d_%H-%M', current_time)
    FILE="forum.chornobyl.com.ua_"+str(cur_date)+".csv"
    print(FILE)
    login=input('Введіть ім\'я користувача:')
    passwd=passprompt('Введіть пароль:')
    session = requests.Session()
    r = session.get(URL, headers = HEADERS)
    session.headers.update({'Referer':URL})
    session.headers.update({'User-Agent':UAG})
    # Осуществляем вход с помощью метода POST с указанием необходимых данных 
    post_request = session.post(URL, {
         'username': login,
         'password': passwd,
         'autologin':'on',
         'sid':sid,
         'redirect':'index.php',
         'login':'Вход',
         'redirect':'./ucp.php?mode=login',
    })
    #Вход успешно воспроизведен и мы сохраняем страницу в html файл
    useragents=open('user-agents.txt','r').read().split('\n')
    proxies=open('proxylist.txt','r').read().split('\n')
    if not "Вы успешно вошли в систему" in post_request.text:
        print('[-] Логін чи пароль невірні!!!')
        sys.exit(-1)
    else:
        print('[+] Ви успішно війшли в систему!!!')
        print_logo()
    startRg=int(input("Введіть початкове значення:"))
    endRg=int(input("Введіть кінцеве значення:"))
    for ui in range(startRg,endRg):
        a = uniform(3,6)
        # print(a)
        sleep(a)
        proxy= {'http':'http://'+choice(proxies)}
        useragent= {'User-Agent': choice(useragents)}
        userLink=user_url+str(ui)
        html=session.get(userLink,headers=useragent)
        get_user_info(html.text,userLink)
    
    save_file(users,FILE)
    os.startfile(FILE)
    with open("hh_success.html","w",encoding="utf-8") as f:
        f.write(post_request.text)
    exit()
    
    
def get_user_info(html,myurl):
    soup=BeautifulSoup(html,'html.parser')
    data={}
    try:
        info=soup.find_all('table',class_='tablebg')[1].find_all('b',class_='gen')
        nick=info[0].text.strip()
        regdate=info[1].text.strip()
        visitdate=info[2].text.strip()
        msgnum=info[3].text.strip()
        data['nick']=nick
        data['regdate']=regdate
        data['visitdate']=visitdate
        data['msgnum']=msgnum
        data['url']=myurl
        print(f"Ник {nick}\n Зарегистрирован {regdate}\n Остнній візит {visitdate}\n Кількість повідомлень: {msgnum}\n")
        try:
            active=soup.find('td',text=re.compile("Наиболее активен в форуме:")).find_next('td').find('b').find('a').text.strip()
        except:
            active=''
        try:
            site=soup.find('td',text=re.compile("Сайт:")).find_next('td').find('b').find('a').text.strip()
        except:
            site=''
        groups=soup.find('td',text=re.compile("Группы:")).find_next('td').text.strip()
        otkuda=soup.find('td',text=re.compile("Откуда:")).find_next('td').text.strip()
        activity=soup.find('td',text=re.compile("Род занятий:")).find_next('td').text.strip()
        interests=soup.find('td',text=re.compile("Интересы:")).find_next('td').text.strip()
        email=soup.find('td',text=re.compile("Адрес e-mail:")).find_next('td').text.strip()
        msnm=soup.find('td',text=re.compile("MSNM/WLM:")).find_next('td').text.strip()
        YIM=soup.find('td',text=re.compile("YIM:")).find_next('td').text.strip()
        aim=soup.find('td',text=re.compile("AIM:")).find_next('td').text.strip()
        icq=soup.find('td',text=re.compile("ICQ:")).find_next('td').text.strip()
        jabber=soup.find('td',text=re.compile("Jabber:")).find_next('td').text.strip()
        data['contacts']=f"{email} {msnm} {YIM} {aim} {icq} {jabber}"
        data['otkuda']=otkuda
        data['groups']=groups
        data['site']=site
        data['active']=active
        data['activity']=activity
        data['interests']=interests
        print('Наиболее активен в форуме: ' + active)
        print('Группи: '+groups)
        print('Звідки: '+otkuda)
        print('Діяльнісь: '+activity)
        print('Сайт: '+site)
        print(f" {email} {msnm} {aim} {YIM} {icq} {jabber}")
        print(f"Посилання на профіль: {myurl}")
        print("-"*100)
        users.append(data)
    except Exception as ex:
        data['otkuda']=''
        data['groups']=''
        data['contacts']=''
        data['active']=''
        data['activity']=''
        data['interests']=''
    except KeyboardInterrupt:
        save_file(users,FILE)
        os.startfile(FILE)
        



def get_content(html):
    soup=BeautifulSoup(html,'html.parser')
    sid= soup.find('input',{'name':'sid'}).get('value').strip()
    login= soup.find('input',{'name':'login','class':'btnmain'}).get('value').strip()
    print(f"sid {sid} login {login}")
    try:
        login_auth(sid)
    except KeyboardInterrupt:
        current_time = time.localtime()
        cur_date=time.strftime('%Y-%m-%d_%H-%M', current_time)
        FILE="forum.chornobyl.com.ua_"+str(cur_date)+".csv"
        save_file(users,FILE)
        os.startfile(FILE)
    for ui in range(6556,6866):
        userLink=user_url+str(ui)
        print(f"userLink {userLink}")
        html=get_request_html(userLink)
        if html.status_code==200: 
            print(html.status_code)
            get_user_info(html.text)
            #print(html.text)
        

def main():
    html=get_html(URL)
    if html.status_code==200:
        get_content(html.text)
        
if __name__=='__main__':
	main()
