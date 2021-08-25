import requests
from random import choice
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
from random import uniform

users=[]
URL='https://forum.cn.ua/index.php?act=Profile&CODE=03&MID='
HEADERS={'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36','accept':'*/*'}
HOST='https://forum.cn.ua'
FILE='forum.cn.ua.csv'
def get_html(url,useragent=None,proxy=None):
    print('get-html')
    r=requests.get(url,headers=useragent,proxies=proxy)
    return r

def get_details(html):

    print('New Forum Member:',end=' ')
    soup=BeautifulSoup(html,'html.parser')
    nick = soup.find('span',class_='pagetitle').text.strip()
    group=soup.find('b',text=re.compile("Группа:")).find_parent('td').find_next_sibling('td',class_='bottomborder').text.strip()
    icq=soup.find('b',text=re.compile("ICQ:")).find_parent('td').find_next_sibling('td',class_='bottomborder').text.strip()
    msn=soup.find('b',text=re.compile("MSN:")).find_parent('td').find_next_sibling('td',class_='bottomborder').text.strip()
    yahoo=soup.find('b',text=re.compile("Yahoo:")).find_parent('td').find_next_sibling('td',class_='bottomborder').text.strip()
    aim=soup.find('b',text=re.compile("AIM:")).find_parent('td').find_next_sibling('td',class_='bottomborder').text.strip()
    regdate=soup.find('b',text=re.compile("Зарегистрировался:")).find_parent('td').find_next_sibling('td',class_='bottomborder').text.strip()
    active=soup.find('b',text=re.compile("Максимально активен в:")).find_parent('td').find_next_sibling('td').find('a').text.strip()
    print("Активен в "+active)
    print('Nick '+nick)
    print(f'Group {group} {icq=} {msn=} {yahoo=} {aim=} {regdate=} {active=}')
    user={
    'nick':nick,'group':group,'icq':icq,'msn':msn,'yahoo':yahoo,'aim':aim,'active':active,'regdate':regdate
    }
    users.append(user)
    print('-'*80)

def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer=csv.writer(file,delimiter=';')
        writer.writerow(['Nick','Группа','ICQ','MSN','Yahoo','AIM','regdate','active'])
        for item in items:
            writer.writerow([item['nick'],item['group'],item['icq'],item['msn'],item['yahoo'],item['aim'],item['regdate'],item['active']])

def main():
    useragents=open('user-agents.txt','r').read().split('\n')
    proxies=open('proxylist.txt','r').read().split('\n')
    for num in range(1,1000):
        a = uniform(3,6)
        print(a)
        sleep(a)
        proxy= {'http':'http://'+choice(proxies)}
        useragent= {'User-Agent': choice(useragents)}
        print(num,end=' ')
        myurl=URL+str(num)
        try:
            html=get_html(myurl,useragent,proxy)
        except:
            continue
        if html.status_code==200:
            print('FORUM USER URL: '+myurl)
            user=get_details(html.text)
            
    save_file(users,FILE)
    os.startfile(FILE)
            

if __name__=='__main__':
	main()