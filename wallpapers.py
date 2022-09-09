#!/usr/bin/env python
import requests
from random import choice
from bs4 import BeautifulSoup
import re

import csv
from time import sleep
from random import uniform
import os
from urllib.parse import urlparse
from PIL import Image, ImageEnhance
from collections import namedtuple
######
import time
import asyncio
from aiohttp import ClientSession
import aiofiles
#######
mycategory=namedtuple('mycategory','address,name')
category='coding'
URL='https://wallpapers.com/{}'.format(category)
HEADERS={'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.5.1525.40','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST='https://wallpapers.com'
imglist=[]
wallpaperdir=r"d:\Users\tonnyr2\Dropbox\Photos\cyberpunkwallpapers"
cntr=1
def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
        
async def make_request(session,wallpaperdirname:str,path:str,imgurl:str)->None:
    mypath=f"{wallpaperdirname}\\{path}"
    try:
        resp = await session.request(method="GET", url=imgurl)
    except Exception as ex:
        print(ex)
        return

    if resp.status == 200:
        async with aiofiles.open(mypath, 'wb') as f:
            await f.write(await resp.read())
        try:
            im = Image.open(mypath)
            newsize = (1280, 795)
            im1=im.resize(newsize)
            im1.save(mypath)
        except:
            print('[-]error')            
            
    
async def get_category(html,myurl):
    soup=BeautifulSoup(html,'html.parser')
    categoryList=[]
    catlist = soup.find_all('a',class_='category__list__item')
    for catItem in catlist:
        if (catItem['href'],catItem['title']) not in categoryList:
            categoryList.append(mycategory(catItem['href'],catItem['title']))
    catList2=soup.find_all('a',class_='caption stretched-link')
    for catItem in catList2:
        if (catItem['href'],catItem.text) not in categoryList:
            categoryList.append(mycategory(catItem['href'],catItem.text)) 
    categoryList=sorted(categoryList,key=lambda ky:ky[1])
    return categoryList
    
            
async def async_get_details(html,myurl,wallpaperdirname:str):
    print("async_get_details")
    soup=BeautifulSoup(html,'html.parser')
    picbox = soup.find_all('picture',class_='picture-box')
    print(f"Кількість шпалер на скачування {len(picbox)}")
    async with ClientSession() as session:
        tasks = []
        for pic in picbox:
            img=pic.find('img',class_='promote')
            src=f"{HOST}{img['src']}"
            if not src in imglist:
                imglist.append(src)
                res= urlparse(src)
                pth=res.path
                pth= os.path.basename(pth)
                tasks.append(make_request(session,wallpaperdirname,path=pth,imgurl=src))
        await asyncio.gather(*tasks)
	
async def main():
    try:
        async with ClientSession() as session:
            html=await session.request(method="GET", url=HOST)
            if html.status == 200:
                sts=html.status
                print(f"{sts=}")
                catList=await get_category(await html.text(),HOST)
                for idx,cat in enumerate(catList,start=1):
                    ln=39-len(str(idx))
                    if idx % 2 >0:
                        print(f"{idx}> {cat.name:<{ln}}",end=' ')
                    else:
                        print(f"{idx}> {cat.name:<{ln}}")
                catIdx=int(input('\nВведіть категорію:'))
                try:
                    catIdx-=1
                    myurl=catList[catIdx].address
                    print(f"{myurl=}")
                    mydirname=input(f'\nВведіть ім\'я папки для збереження шпалер({os.getcwd()}):')
                    if not os.path.exists(mydirname) or not os.path.isdir(mydirname):
                        print('[-]Папки не існувало зараз створимо')
                        os.mkdir(mydirname)
                    html=get_html(myurl,useragent=HEADERS,proxy=None)
                    sts=html.status_code
                    start = time.time()            
                    
                    await async_get_details(html.text,myurl,mydirname)
                    print('{} s'.format(time.time() - start))
                    return
                except ValueError:
                    print('Введіть ціле число індекс категорії')
                    return
                except KeyError:
                    print(f'Індекс категорії виходить за межі більше за {len(catList)}')
                    return                
                except IndexError:
                    print(f'Індекс категорії виходить за межі більше за {len(catList)}')
                    return
        # print(catList)
    except:
        pass
	

if __name__=='__main__':
    clr()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())