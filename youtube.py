#!/usr/bin/env python
import requests
from random import choice
from bs4 import BeautifulSoup
import re
import lxml
import json
import csv
import os


url=input('Enter youtube url:')


HEADERS={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Referer':'http://bitly.ws/',
'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36',
'Accept-Encoding' :'gzip, deflate',
'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7'
}

res=requests.get(url,headers=HEADERS,stream=True,timeout=10)

if res.status_code==200:
    html=res.text
    res1=re.search(r'\"canonicalBaseUrl\":\"([^\"]+)\"',html)
    if res1:
        print(str(res1))
        chan=f"https://youtube.com{res1[1]}"
        print(chan)# {res1[len(res1)-1]}")
        ytch=requests.get(chan,headers=HEADERS,stream=True,timeout=10)
        if ytch.status_code==200:
            res1=re.search(r'<title>([^>]+)<\/title>',ytch.text)
            if res1:
                print(res1[1])
    
    
res2 = re.findall(r'owner\":{\"videoOwnerRenderer\":{"thumbnail\":{\"thumbnails\":\[({[^{}\[\]]+}),({[^{}\[\]]+})',html)
if res2:
    for img in res2:
        print(img)
        realPic=img[1]
        chanImg=re.search(r'(https://yt3\.ggpht\.com/[^"]+)",',realPic)
        
        print(realPic)
        if chanImg:
            print(chanImg[1])
            kartinka=chanImg[1]
            with open("chanimg.jpg", 'wb') as handle:
                response = requests.get(kartinka, stream=True)
                hdrs=response.headers
                print(f"Content-Type {hdrs['Content-Type']}")
                if not response.ok:
                    print("ok")
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
                    
            os.startfile("chanimg.jpg")