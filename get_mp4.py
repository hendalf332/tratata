#!/usr/bin/env python
import requests
import sys
import re
import colorama
import os
if os.name=='nt':
    colorama.init(convert=True)
from utils.decorators import MessageDecorator
from utils.provider import APIProvider

mesgdcrt=MessageDecorator("icon")

cnt=0
#url=''
file_lst=["mp4","mp3",'ico','gif','jpg','jpeg']

for link in sys.argv:
    res=re.search(r'(https?://([\w\-\_]+\.){1,2}\w+)/',link)
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
        expr='([^"]+\.mp4)'
        ext_dict={}
        prev_res=''
        results=re.findall(r'"[^"]+\.([\w\d]{1,4})"',html)
        for res in results:
            if res not in ext_dict:
                ext_dict[res]=1
            else:
                ext_dict[res]+=1
            # print(res)
        for ky,val in ext_dict.items():
            print(ky,f" {val} ",end='')
        
        print("\n","#"*80)
        file_lst=list(map(str, input("Введіть список типів файлів для пошуку:").lower().split()))
        for ext in file_lst:
            files=re.findall(r'"([^"]+\.'+ext +')"',html)
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
    cnt+=1
