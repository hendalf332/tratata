#!/usr/bin/env python
# -*- coding: utf8 -*-
import asyncio
import logging
###########################################
import config
import weirdbot_keyboard        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ keyboard.py
import sqlshortlinks
###########################################
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from aiogram.types import InputTextMessageContent,InlineQueryResultArticle
#######################
import socket
import re
import io
import requests
import csv
import sqlite3
from bs4 import BeautifulSoup
######################
from aiogram.dispatcher import FSMContext                            ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters import Command                        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.contrib.fsm_storage.memory import MemoryStorage        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters.state import StatesGroup, State        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM

######################
class searchstates(StatesGroup):
    srch = State()
    titleSrch = State()
    urlSrch = State()
storage = MemoryStorage() # FOR FSM
    
# Объект бота
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot,storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
LOGFILE='shortlinks.txt'

db=sqlshortlinks.SQLShortLinks('shortlinks.db')

hlpmsg="""
Бот скорочувач посилань онлайн 
Задайте мені правильний URL і я видам вам коротке посилання на нього
<strong color="red">Увага:</strong>
URL з : # , Кириличні символи та деякі інші не приймаються
URL повинен починатися з http або https в залежності який протокол підтримується
Якщо не працює з https спробуйте http
"""

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    print(query.from_user.id)
    uid=query.from_user.id
    if len(query.query) == 0:
        print("Запит відсутній")
        return
    else:
        srchtxt=query.query.strip().lower()
        uname="{0.first_name}_{0.last_name}_{0.username}".format(query.from_user)
        print(f"Inline запит {query.query} користувача {uname}")
        #urllist= list(csv.reader(open(LOGFILE,encoding="utf-8"),delimiter=';'))
        urllist=db.get_links(srchtxt)
        reslist=[]
        for i,line in enumerate(urllist):
            slOwner=line[0]
            urlstr=line[1]
            title=line[3]
            if (srchtxt in urlstr.lower() or srchtxt in title.lower() ):# and ( uname==slOwner or query.from_user.id==config.adminid ):
                reslist.append(
                InlineQueryResultArticle(
                    id=i+1,
                    title=f'{urlstr} {line[3]}',
                    input_message_content=InputTextMessageContent(
                        message_text=f'{line[0]} {line[2]} {line[3]}'
                    )
                )
                )
        if query and not reslist:
            reslist.append(
                InlineQueryResultArticle(
                    id=999,
                    title='[-]Нічого нема!!!',
                    input_message_content=InputTextMessageContent(message_text=f'[-]Нічого не знайшлося'),
                )
            )
        await bot.answer_inline_query(query.id, results=reslist, cache_time=20) 
                  

@dp.message_handler(commands=['help'])
async def help(message):
    #await bot.send_message(message.chat.id, hlpmsg)
    await message.answer(hlpmsg)

@dp.message_handler(content_types=['text'],state=searchstates.urlSrch)
async def urlsrchCmd(message: types.Message, state: FSMContext):  
    srchtxt=message.text.strip().lower()
    print(f"UrlCmd {srchtxt}")
    cid=message.chat.id
    cnt=0
    uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
    urllist= db.get_urllinks(srchtxt)
    reslist=[]
    for line in urllist:
        slOwner=line[0]
        urlstr=line[1]
        if srchtxt.lower() in urlstr.lower() and uname==slOwner:
            lstMsg=f"{line[0]} ShortLink {line[2]} Title {line[3]}"
            reslist.append(list(line))
            await message.answer(lstMsg)
            cnt+=1
        elif cid==config.adminChat and srchtxt in urlstr:
            lstMsg=f"{line[0]} ShortLink {line[2]} Title {line[3]}"
            await message.answer(lstMsg)
            reslist.append(list(line))
            cnt+=1
    if cnt==0:
        await message.answer("[-]Нажаль нічого не знайдено!!!")
    else:
        await message.answer(reslist)
        await message.answer(f"[+]Знайдено {cnt} записів")
    await message.answer('Виберіть тип пошуку:')
    await searchstates.srch.set()

@dp.message_handler(content_types=['text'],state=searchstates.srch)
async def srchCmd(message: types.Message, state: FSMContext):   
    if message.text=='🔎Шукати по URL':
        await message.answer('Введіть підстроку з URL:')
        await searchstates.urlSrch.set()
        return
    elif message.text=='🔎Шукати по Тайтлам':
        await message.answer('Введіть підстроку з Title сторінки:')
        await searchstates.titleSrch.set()
        return
    elif message.text=='🔙Назад':
        await message.answer('Введіть URL для скорочення:',reply_markup=weirdbot_keyboard.start,parse_mode='Markdown')
        await state.finish()
    else:
        await message.answer('Введіть команду з кнопок клавіатури:',reply_markup=weirdbot_keyboard.poshuk,parse_mode='Markdown')
 

    
    
@dp.message_handler(content_types=['text'],state=searchstates.titleSrch)
async def titleCmd(message: types.Message, state: FSMContext):  
    srchtxt=message.text.strip().lower()
    print(f"TitleCmd {srchtxt}")
    cid=message.chat.id
    uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
    #urllist= list(csv.reader(open(LOGFILE,encoding="utf-8"),delimiter=';'))
    urllist=db.get_titlelinks(srchtxt)
    cnt=0
    for line in urllist:
        slOwner=line[0]
        titleStr=line[3]
        if srchtxt.lower() in titleStr.lower() and uname==slOwner:
            lstMsg=f"{line[0]} ShortLink {line[2]} Title {line[3]}"
            await message.answer(lstMsg)
            cnt+=1
        elif cid==config.adminChat and srchtxt.lower() in titleStr.lower():
            lstMsg=f"{line[0]} ShortLink {line[2]} Title {line[3]}"
            await message.answer(lstMsg)
            cnt+=1
    if cnt==0:
        await message.answer("[-]Нажаль нічого не знайдено!!!")
    else:
        await message.answer(f"[+]Знайдено {cnt} записів")
    await message.answer('Виберіть тип пошуку:')
    await searchstates.srch.set()
            

@dp.message_handler(commands=['list'])
async def hlist(message):
    #await bot.send_message(message.chat.id, hlpmsg)
    uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
    cid=message.chat.id
   # urllist= list(csv.reader(open(LOGFILE),delimiter=';'))
    urllist = db.get_alllinks()
    if len(urllist)>300:
        urllist=urllist[:300]
    for line in urllist:
        slOwner=line[0]
        lstMsg=f"Користувач {line[0]} ввів адресу {line[1]} ShortLink {line[2]} тайтл {line[3]}"
        print(lstMsg)
        if slOwner==uname:
            await message.answer(lstMsg,parse_mode=types.ParseMode.HTML)
        if slOwner!=uname and cid==config.adminChat:
            await message.answer(lstMsg,parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands="start", state=None)
async def welcome(message):
    w_sticker = io.open(
			'sticker1.webp', 'rb')
    await message.answer_sticker(w_sticker)
    await message.answer(f"ПРИВЕТ, *{message.from_user.first_name},* БОТ ShortUrlLink РАБОТАЕТ",reply_markup=weirdbot_keyboard.start, parse_mode='Markdown')

@dp.message_handler(content_types=['text'], state=None)
async def get_message(message):
    if message.chat.type == 'private':
        if message.text=='❓ Довідка':
            await message.answer(hlpmsg)
            return
        if message.text=='🔗 Читати історію':
            await hlist(message)
            return
        if message.text=='🔎Пошук URL':
            await message.answer('Виберіть тип пошуку:',reply_markup=weirdbot_keyboard.poshuk,parse_mode='Markdown')
            await searchstates.srch.set()
            return
        if message.text=='🔙Назад':
            await message.answer('Введіть URL для скорочення:',reply_markup=weirdbot_keyboard.start,parse_mode='Markdown')
    try:
        link=message.text
        res=re.search(r'(https?://([\w\-\_]+\.){1,4}\w+)(?:/|$)',link)
        if res:
            uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
            if db.url_exists(uname,link):
                dbres=db.get_shortlinks(link)
                await message.answer(f"Посилання {link} вже існує")
                print(dbres)
                for lnk in list(dbres):
                    print(f"Посилання {lnk[0]} на {link} вже існує {lnk[1]}")
                    await message.answer(f"Посилання {lnk[0]} на {link} вже існує  {lnk[1]}")
                return
            url=link
            forbiddensymbs="йцукенгшщзхїєждлорпавіфячсмитьбюыэъё№#"
            for smb in forbiddensymbs:
                if smb in link:
                    await message.answer("Мій бот не приймає кириличних та інших символів")
                    print("Мій бот не приймає кириличних та інших символів")
                    return
            target_host = "bitly.ws"
            params='/create.php?url='+url
            print(target_host) 
            target_port = 80  # create a socket object 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
             
            # connect the client 
            client.connect((target_host,target_port))  
             
            # send some data 
            request = f"GET {params} HTTP/1.1\r\nHost:{target_host}\r\n\r\n"
            print(request)
            client.send(request.encode())  
             
            # receive some data 
            response = client.recv(4096)  
            http_response = repr(response)
            http_response_len = len(http_response)
             
            #display the response
            print("[RECV] - length: %d" % http_response_len)
            print(http_response)
            NEWHEADERS={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer':'http://bitly.ws/',
            'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36',
            'Accept-Encoding' :'gzip, deflate',
            'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7'
            }
            res=re.search(r'(http://[\w\/\.]+)',http_response)
            if res:
                tinyurl=res.group(0)
                print(f"TinyUrl {tinyurl}")
                res=requests.get(tinyurl,headers=NEWHEADERS,stream=True,timeout=10)
                if res.status_code==200:
                    html=res.text
                    print('Вдалося')
                    soup=BeautifulSoup(html,'lxml')
                    try:
                        tinyurl=soup.find('div',id='clip-text').find('b').text.strip()
                        uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
                        
                        print(tinyurl)
                        title=''
                        try:
                            res2=requests.get(link,headers=NEWHEADERS,stream=True,timeout=10)
                            if res2.status_code==200:
                                linkHtml=res2.text
                                soup2=BeautifulSoup(linkHtml,'lxml')
                                title=soup2.find('title').text.strip()
                        except:
                            title=''
                        answer=f"[+] Success {uname} {link} {tinyurl} {title}"
                        await message.answer(answer )
                        print(answer)
                        
                        urllist= db.get_alllinks()
                        urlset = list()
                        for line in urllist:
                            urlset.append(line[1].strip())
                        if len(urlset)>10:
                            urlset=urlset[-10:]

                        if not db.url_exists(uname,link):
                            db.add_url(uname,link,tinyurl,title)
                        else:
                            dbres=db.get_shortlinks(link)
                            for lnk in list(dbres):
                                print(f"Посилання {lnk[0]} на {link} вже існує Тайтл {lnk[1]}")
                                await message.answer(f"Посилання {lnk[0]} на {link} вже існує Тайтл {lnk[1]}")
                    except:
                        print('Не вдалося')
                        await message.answer('Не вдалося')
        else:
            answer="Введіть валідний URL!!!"
            await message.answer(answer)
            return

    
    except:
        await message.answer('Введіть URL адрессу')

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
