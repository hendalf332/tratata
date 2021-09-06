#!/usr/bin/env python
import requests
import sys
import re

cnt=0
for link in sys.argv:
    if cnt>0:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        res = requests.get(link,headers=headers,stream=True,timeout=20)
        #print(res)
        html = res.text
        expr='([^"]+\.mp4)'
        if(html.find(".mp4") != -1):
            res=re.search(r'"([^"]+\.mp4)"',html)
            if res:
                video_url=res.group(1)
                print(video_url)
    cnt+=1
