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
file_lst=["mp4","mp3",'ico','gif','jpg','jpeg']
file_lst=list(map(str, input(mesgdcrt.CommandMessage("Введіть список типів файлів для пошуку:").lower().split())))
for link in sys.argv:
    res=re.search(r'(https?://(\w+\.){1,2}\w+)/',link)
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
        prev_res=''
        results=[]
        for ext in file_lst:
            files=re.findall(r'"([^"]+\.'+ext +')"',html)
            if files:
                for res in files:
                    video_url=res
                    video_url=re.sub(r"^/",url+"/",video_url)
                    if video_url not in results:
                        results.append(video_url)
                        print(video_url)
    cnt+=1
