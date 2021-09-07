#!/usr/bin/env python
import requests
import sys
import re
import colorama
import os
if os.name=='nt':
    colorama.init(convert=True)
     
cnt=0
file_lst=[]
href_list=[]
not_ext=[]#'com','net','org','ru','us','ua','edu','it','de','bg','nl','pl','fr','at','es','hu']
for link in sys.argv:
    res=re.search(r'(https?://([\w\-\_]+\.){1,4}\w+)(?:/|$)',link)
    if res:
        url=res.group(1)
    if cnt>0:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        res = requests.get(link,headers=headers,stream=True,timeout=20)
        html = res.text
        # print(html)
        ext_dict={}
        mail_list=[]
        tel_list=[]
        href_list=[]
        results=re.findall(r'href="([^\"]+)"',html)
        for res in results:
            if res not in href_list:
                res=re.sub(r"^/",url+"/",res)
                href_list.append(res) 
        results=re.findall(r'(https?:[^"\'\s]+)["\s\']',html)
        for res in results:
            if res not in href_list:
                res=re.sub(r"^/",url+"/",res)
                href_list.append(res)         
                
        results=re.findall(r"\+?(\d{,2}(?:\(\d{3,4}\))[\s\-](?:\d{2,3}[\s\-]?)(?:\d{2,3}[\s\-]){1,3}\d{2,3})[\s<\"\']",html)
        for res in results:
            if res not in tel_list:
                tel_list.append(res)
                
        results=re.findall(r"\+\d{10,15}",html)
        for res in results:
            if res not in tel_list:
                tel_list.append(res)
                #print(res)
        results=re.findall(r"([a-zA-Z0-9+_.-]+@(?:[a-zA-Z0-9][a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+)",html)
        for res in results:
            if res not in mail_list:
                mail_list.append(res)
                #print(res)
        print('Список телефонів:')
        print(tel_list)
        print('Список емейлів:')
        print(mail_list)
        results=re.findall(r'"[^"?\s]*/[^"?\s]+\.([\w\d]{1,4})["?/]',html)
        for res in results:
            if res not in not_ext:
                if res not in ext_dict:
                    ext_dict[res]=1
                else:
                    ext_dict[res]+=1
        ci=0
        for ky,val in ext_dict.items():
            print("<"+ky,f" {val}>",end='')
            ci+=1
            if ci%5==0:
                print()
        print("\n","#"*80)
        file_lst=list(map(str, input("Введіть список типів файлів для пошуку:").lower().split()))
        for ext in file_lst:
            files=re.findall(r'"([^"?\s]*/[^"?\s]+\.'+ext +')[?"/]',html)
            if files:
                for res in files:
                    video_url=res
                    video_url=re.sub(r"^/",url+"/",video_url)
                    if not re.match(r"^https?://",video_url):
                        video_url=re.sub(r"^",url+"/",video_url)
                    if video_url not in results:

                        if video_url not in results:
                            results.append(video_url)
                            print(video_url)
                print("#"*80)
    cnt+=1
input()
for el in href_list:
    print(el)
