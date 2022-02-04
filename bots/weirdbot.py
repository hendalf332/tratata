#!/usr/bin/env python
# -*- coding: utf8 -*-
################################################################################################################################
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,InputTextMessageContent,InlineQueryResultArticle
from aiogram.utils.exceptions import BotBlocked,InvalidQueryID
from aiogram.types.sticker import Sticker
import asyncio
#################################################################################################################################
 
######################################################################
from aiogram.dispatcher import FSMContext                            
from aiogram.dispatcher.filters import Command                       
from aiogram.contrib.fsm_storage.memory import MemoryStorage        
from aiogram.dispatcher.filters.state import StatesGroup, State        
######################################################################
 
######################
import weirdbot_keyboard        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ keyboard.py
import config
import sqlshortlinks
######################

#######################
from mega import Mega
import requests
import psycopg2
import sys
import re
import os
import csv
from time import sleep
from time import time
import random
import io
from os import getenv
#######################
 
import logging # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ
storage = MemoryStorage() # FOR FSM
bot_token = config.WEIRDURLBOTTOKEN

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

db=sqlshortlinks.PGShortLinks()
mega=Mega()
mg = mega.login(config.email, config.passwd)

@dp.errors_handler(exception=InvalidQueryID)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):

    print(f"Час запиту вийшов чи ідентифікатор запиту ЗАСТАРИЙ!\nСообщение: {update}\nОшибка: {exception}")

    return True

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

href_list=[]
not_ext=[]
start=time()

soclist=[]
ext_dict={}
mail_list=[]
tel_list=[]
cmd_dict={}
file_results=[]
uname=''
resultat=''

socnet_list=('facebook.com','vk.com','vm.tiktok.com','instagram.com','odnoklassniki.ru','ok.ru','youtube.com','tiktok.com','t.me')
weblinks=('com','net','org','ru','us','ua','edu','it','de','bg','nl','fr','at','es','hu')
hlpmsg="""
Задайте мені строку параметр URL сторінки 
Я розпарщю її вилучу корисні контактні данні:
Соціальні мережі,Номери Телефонів, адреси електронних скриньок,
розширення файлів які зустрічаються в коді сторінки.
Якщо ви задасте 2 параметри 
наприклад https://2ip.ru js,css,svg 
(URL та список розширень через кому)
Тоді я вилучу ще посилання на файли вибраних розширень
Нова Функція: Бот Зберігає історію
Якщо клацнете "Читати історію"
переглянете список всіх успішних URL команд
---------------------------------------------
Результати: &lt;png 7&gt; &lt; css 2 &gt;&lt;js 11&gt;&lt;gif 3&gt;
Означають що файли з розширенням png зустрічаються
в коді сторінки 7 разів, а css 2,
а js файлів в коді 11 раз,а gif файли зустрічаються 3 рази

get_mp4_link +URL на сторінку з відео спробує вилучити 
посилання на відео якщо там встановленний kt_player
"""

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    print(query.from_user.id)
    uid=query.from_user.id
    if len(query.query) == 0:
        print("Запит відсутній")
    else:
        print(f"Inline запит {query.query}")
        link=query.query
        result_id: str = "Відовідь"
        res=re.search(r'^(https?://([\w\-\_]+\.){1,4}\w+)(?:/|$|\s*(?:\w+,?)*$)',link)
        if res:
            url=res.group(1)
            flg=False
            if " " in query.query:
                flg=True
            await get_url_info(query,flg)
            resultat=url+'\nСписок телефонів:'+str(set(tel_list))+'\n'+'Список емейлів:'+str(mail_list) + '\nСписок соцмере:'+str(soclist)+'\nСписок файлів:' + str(file_results)
            resultat+='\n'
            for ky,val in ext_dict.items():
                resultat+=f"&lt;{ky} {val}&gt;"
            if len(resultat)>4000:
                resultat=resultat[:4000]
            input_content = InputTextMessageContent(resultat)
            item = InlineQueryResultArticle(
            id=query.from_user.id,
            title=f'Result {link!r}',
            input_message_content=input_content,
        )
            await bot.answer_inline_query(query.id, results=[item], cache_time=20) 
            for telnum in tel_list:
                if db.tel_exists(telnum)==0:
                    db.add_tel(telnum)
                else:
                    print(f"[-] Вже існує {telnum} ")
                    
            for mail in mail_list:
                if db.email_exists(mail)==0:
                    db.add_email(mail)
                else:
                    print(f"[-] Вже існує {mail} ")

        else:
            answer="Введіть валідний URL!!!"
            input_content = InputTextMessageContent(query.query)
            item = InlineQueryResultArticle(
            id=result_id,
            title=f'Result {answer!r}',
            input_message_content=input_content,
        )
        # don't forget to set cache_time=1 for testing (default is 300s or 5m)
   
@dp.message_handler(commands=['readurls'])
async def readUrls(message,query=''):
    uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
    cmdlist=[]
    folder = mg.find('logs')
    logfile = mg.find(uname)
    if logfile:
        print(f'[+] Файл {uname} існує')
        mg.download(logfile)
    if os.path.exists(uname):
        file = list(csv.reader(open(uname,encoding="utf-8"),delimiter=';'))
        # print(file)
        for row in file:
            cmdlist.append(row[0])
        cnt=1
        if len(cmdlist)>10:
            cmdlist=cmdlist[-10:]
            for el in cmdlist:
                await bot.send_message(message.chat.id,f"#{cnt} {el}",reply_markup=weirdbot_keyboard.viewUrl, parse_mode='Markdown')
                cnt+=1
        else:
            for el in cmdlist:
                await bot.send_message(message.chat.id,f"#{cnt} {el}",reply_markup=weirdbot_keyboard.viewUrl, parse_mode='Markdown')
                cnt+=1
    else:
        if cmd_dict[uname]:
            for cmd in cmd_dict:
                await bot.send_message(message.chat.id, cmd)

@dp.message_handler(Command("start"), state=None)
async def welcome(message):
    tel_list.clear()
    mail_list.clear()
    href_list.clear()
    ext_dict.clear()
    uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
    cmd_dict[uname]=list()
    w_sticker = io.open(
			'sticker2.webp', 'rb')
    await message.answer_sticker(w_sticker)
    try:
        me=await bot.get_me()
        uname=message.from_user.username
        print(me.first_name)
        print(uname)
        #await message.answer(f"Вітаємо {message.from_user.first_name} ,!\n Я - {me.username}\n /help довідка", reply_markup=weirdbot_keyboard.start, parse_mode='Markdown')
        await bot.send_message(message.chat.id, f"Вітаємо {message.from_user.first_name} ,!\n Я - {me.username}\n /help довідка", reply_markup=weirdbot_keyboard.start, parse_mode='Markdown')
    except:
        return


@dp.message_handler(commands=['help'])
async def help(message):
    #await bot.send_message(message.chat.id, hlpmsg)
    await message.answer(hlpmsg)

@dp.message_handler(commands=['emails'])
async def emails(message):
    #await bot.send_message(message.chat.id, hlpmsg)
    emaillist=db.get_allemails()
    for eml in emaillist:
        await message.answer(eml[0])


@dp.message_handler(commands=['tels'])
async def emails(message):
    #await bot.send_message(message.chat.id, hlpmsg)
    telnumlist=db.get_alltels()
    for telnm in telnumlist:
        await message.answer(telnm[0])

@dp.message_handler(content_types=['text'])
async def get_message(message):
    if message.chat.type == 'private':
        if message.text=='❓ Довідка':
            await bot.send_message(message.chat.id,hlpmsg)
            return
        if message.text=='🔗 Читати історію':
            await readUrls(message)
            return
        mtch=re.search(r'^get_mp4_link',message.text)
        if mtch:
            msgtxt=message.text
            msgtxt=msgtxt.split(' ')
            msgtxt=msgtxt[1]
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            }

            res = requests.get(msgtxt,headers=headers,stream=True,timeout=5)
            #print(res)
            html = res.text

            if(html.find("license_code:") != -1):
                t1 = html.split("license_code: '")
                t2 = t1[1].split("'")
                d = t2[0]
                d1 = d.replace('0', '1')
                
                f = d1[1:]
                
                c = 16

                t1 = html.split("function/0/")
                t2 = t1[len(t1)-1].split("'")
                orig = t2[0]
                
                j = int(len(f) / 2)
                
                k = int(f[0: j + 1])
                l = int(f[j:])
                g = l - k

                if g < 0:
                    g = - g

                f = g
                g = k - l

                if g < 0:
                    g = -g

                f += g
                f = int(f * 2)

                f = "" + str(f)
                i = int(c / 2) + 2
                m = ""
                g = 0
                while g < j+1:
                    h = 1
                    while h <= 4:
                        n = int(d[g + h]) + int(f[g])
                        if n >= i:
                            n -= i
                        m = str(m) + str(n)
                        h = h + 1
                    g = g + 1

                t1 = orig.split("/")
                j = t1[5]

                h = j[0:32]
                i = m

                j = h
                k = len(h) - 1
                while k >= 0:
                    l = k
                    m = k

                    i = str(i)
                    while m < len(i):
                        l = l + int(i[m])
                        m = m + 1

                    while l >= len(h):
                        l = l - len(h)

                    n = ""
                    o = 0
                    while o < len(h):
                        if o == k:
                            n = n + h[l]
                        else:
                            if o == l:
                                n = n + h[k]
                            else:
                                n = n + h[o]

                        o = o + 1

                    h = n

                    k = k - 1

                link = orig.replace(j, h)

                try:
                    response = requests.get(link,headers=headers,stream=True,timeout=20)
                except:
                    await bot.send_message(message.chat.id,'none. Link Not found.')
                    print('Exception!!! none. Link Not found.')
                    return
                
                if response.history:
                    final_result = response.url
                    await bot.send_message(message.chat.id,final_result)
                    print(final_result)
                else:
                    await bot.send_message(message.chat.id,"Request was not redirected")
                    print("Request was not redirected")
                    return
            else:
                await bot.send_message(message.chat.id,'none. Link Not found.')
                print('none. Link Not found.')
            return
    answer=''
    cnt=0
    html=''
    file_lst=[]

    try:
        addresses=message.text
        #print(f"{addresses}")
        address=message.text.split(' ')
        if len(address)==1:
            link=address[0]
        elif len(address)==2:
            link=address[0]
            file_lst=list(map(str, address[1].lower().split(',')))
        else:
            await bot.send_message(message.chat.id,"Введіть URL або URL та список розширень напр. css,js,php...")
            return
        res=re.search(r'(https?://([\w\-\_]+\.){1,4}\w+)(?:/|$)',link)
        if res:
            url=res.group(1)
            print(f'url {url} {link}')
        else:
            answer="Введіть валідний URL!!!"
            await bot.send_message(message.chat.id, answer)
            return
        HEADERS2 = {
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        res = requests.get(link,headers=HEADERS2,verify=False)#,stream=True,timeout=5)

        if res.status_code!=200:
            print(f"status code {res.status_code}")
            await bot.send_message(message.chat.id,f"Вибачте URL {link} наразі не відповідає!!!")
            return
        else:
            print(res.status_code)
            
        print(f"status code")
        print(f"Кодировка {res.encoding}")
        res.encoding="UTF-8"
        print(f"Кодировка {res.encoding}")
        html = res.text
        # with open("index.html", "w",encoding="utf-8") as file:
            # file.write(html)
        # with open("index.html",encoding="utf-8") as file:
            # html = file.read() 
        for soclnk in socnet_list:
            results=re.findall(r'(https?:\\?/\\?/(?:w{3}\.)?'+ soclnk +r'\\?/[\w\d\-_]+)[\s<\"\']',html)
            for res in results:
                if res not in soclist:
                    res=re.sub(r"\\/","/",res)
                    soclist.append(res)
            results=re.findall(r'(https?:[^"\'\s]+)["\s\']',html)
            for res in results:
                if res not in href_list:
                    res=re.sub(r"^/",url+"/",res)
                    res=re.sub(r"\\/","/",res)
                    href_list.append(res)    

        results= re.findall(r"\+?(\d{,2}(?:\(\d{3,4}\))[\s\-](?:\d{2,3}[\s\-]?)(?:\d{2,3}[\s\-]){1,3}\d{2,3})[\s<\"\']",html)
        for res in results:
            if res not in tel_list:
                if not re.match(r'^\+',res):
                    res=re.sub(r'^','+',res)
                tel_list.append(res)
                
        results=re.findall(r"\+\d{10,15}",html)
        for res in results:
            if res not in tel_list:
                tel_list.append(res)
                   
                
        results=re.findall(r"([a-zA-Z0-9+_.-]+@(?:[a-zA-Z][a-zA-Z0-9-]+\.)+[a-zA-Z][a-zA-Z0-9-]+)",html)
        for res in results:
            if res not in mail_list:
                mail_list.append(res)
        results=re.findall(r'href="([^\"]+)"',html)
        for res in results:
            if res not in href_list:
                res=re.sub(r"^/",url+"/",res)
                href_list.append(res) 

        results= re.findall(r'(["\'][^\'"?\s]+\.([a-z][\w\d]{0,6})["\'?/])',html)
        # print(results)
        results=list(set(results))
        for res in results:
            if res[1] not in not_ext:
                if res[1] not in ext_dict:
                    ext_dict[res[1]]=1
                else:
                    ext_dict[res[1]]+=1

        await message.answer('Список телефонів:')
        await message.answer(str(set(tel_list)))
        await message.answer('Список емейлів:')
        await message.answer(str(mail_list))
        await message.answer('Список соцмереж')
        for soc in soclist:
            await message.answer(soc)
        ci=0
        answer=''
        for ky,val in ext_dict.items():
            answer+=f"&lt;{ky} {val}&gt;"
            ci+=1
        await message.answer(answer)
        print(f"{answer}")
        await message.answer("#"*80)

      

        for telnum in tel_list:
            if db.tel_exists(telnum)==0:
                db.add_tel(telnum)
            else:
                print(f"[-] Вже існує {telnum} ")
                
        for mail in mail_list:
            if db.email_exists(mail)==0:
                db.add_email(mail)
            else:
                print(f"[-] Вже існує {mail} ")

        results.clear()
        for ext in file_lst:
            files=re.findall(r'["\']([^\'"\s]+\.'+ext +')[?"\'/]',html)
            if files:
                for res in files:
                    video_url=res
                    video_url=re.sub(r"^/",url+"/",video_url)
                    if not re.match(r"^https?:",video_url):
                        video_url=re.sub(r"^",url+"/",video_url)
                    video_url=re.sub(r"\\/","/",video_url)
                    if video_url not in results:

                        if video_url not in results:
                            results.append(video_url)
                            await message.answer(video_url)
                            print(video_url)
                print("#"*80)
                

        
        tel_list.clear()
        mail_list.clear()
        href_list.clear()
        ext_dict.clear()
        soclist.clear()
#################################################
        uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
        print(f"uname {uname}")
        folder = mg.find('logs')
        logfile = mg.find(uname)
        
        if logfile:
            print(f'[+] Файл {uname} існує')
            mg.download(logfile)
        folder = mg.find('logs')
        file = mg.find(uname)
        if file:
            print('[+]Видалення файлу')
            print(mg.destroy(file[0]))
        else:
            print('[-]Не Знайшовся')
        cmd_dict[uname].append(addresses)
        me=await bot.get_me()
        print("Користувач: {0.first_name}".format(message.from_user,me))
        print("Користувач: {0}".format(message.from_user,me))
        print(f"{uname}")
        print(addresses,url)
        
        urllist= list(csv.reader(open(uname),delimiter=';'))
        urlset = list()
        for line in urllist:
            urlset.append(line[0].strip())
        if len(urlset)>10:
            urlset=urlset[-10:]
        print(f'open {uname}')
        with open(uname,"a",encoding="utf-8", newline='') as file:
                writer=csv.writer(file,delimiter=';')
                if addresses not in urlset:
                    writer.writerow((
                    addresses,
                    url
                    ))
                    print(file)
                    
        file=mg.upload(uname,folder[0])
######################################          
        print(f"{addresses}")

    except:
        await bot.send_message(message.chat.id, message.text)


@dp.callback_query_handler(text_contains='viewAddr')
async def viewAddr(call: types.CallbackQuery):
    print(call.message)
    msg=call.message.text
    num=msg.split(' ')
    num=len(num[0])
    msg=msg[num+1:]
    
    print(str(num)+' '+msg)
    call.message.text=msg
    await get_message(call.message)
    await call.answer()
    
@dp.callback_query_handler(text_contains='viewOnlyUrl')
async def viewOnlyUrl(call: types.CallbackQuery):
    print(f" viewOnlyUrl {call.message.text}")
    msg=call.message.text
    msg=msg.split(' ')
    print(msg[1])
    call.message.text=msg[1]
    await get_message(call.message)
    await call.answer()


async def get_url_info(query,flg):
    print(f"url {query.query} is ok")
    await bot.send_message(query['from'].id,f"url {query.query} is ok")
    try:
        addresses=query.query
        #print(f"{addresses}")
        tel_list.clear()
        mail_list.clear()
        href_list.clear()
        ext_dict.clear()
        soclist.clear()
        file_results.clear()
        address=query.query.split(' ')
        if len(address)==1:
            link=address[0]
        elif len(address)==2:
            link=address[0]
            file_lst=list(map(str, address[1].lower().split(',')))
        else:
            print("Введіть URL або URL та список розширень напр. css,js,php...")
            return
        res=re.search(r'(https?://([\w\-\_]+\.){1,4}\w+)(?:/|$)',link)
        if res:
            url=res.group(1)
        else:
            answer="Введіть валідний URL!!!"
            print(answer)
            return
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        #res = requests.get(link,headers=headers,stream=True,timeout=5)
        res= requests.get(link,headers=headers,verify=False)
        if res.status_code!=200:
            print(f"Вибачте URL {link} наразі не відповідає!!!")
            return
        res.encoding="UTF-8"
        html = res.text
        if flg!=True:
            for soclnk in socnet_list:
                results=re.findall(r'(https?:\\?/\\?/(?:w{3}\.)?'+ soclnk +r'\\?/[\w\d\-_]+)[\s<\"\']',html)
                for res in results:
                    if res not in soclist:
                        res=re.sub(r"\\/","/",res)
                        soclist.append(res)
                results=re.findall(r'(https?:[^"\'\s]+)["\s\']',html)
                for res in results:
                    if res not in href_list:
                        res=re.sub(r"^/",url+"/",res)
                        res=re.sub(r"\\/","/",res)
                        href_list.append(res)    

            results= re.findall(r"\+?(\d{,2}(?:\(\d{3,4}\))[\s\-](?:\d{2,3}[\s\-]?)(?:\d{2,3}[\s\-]){1,3}\d{2,3})[\s<\"\']",html)
            for res in results:
                if res not in tel_list:
                    if not re.match(r'^\+',res):
                        res=re.sub(r'^','+',res)
                    tel_list.append(res)
                    
            results=re.findall(r"\+\d{10,15}",html)
            for res in results:
                if res not in tel_list:
                    tel_list.append(res)
                           
            results=re.findall(r"([a-zA-Z0-9+_.-]+@(?:[a-zA-Z][a-zA-Z0-9-]+\.)+[a-zA-Z][a-zA-Z0-9-]+)",html)
            for res in results:
                if res not in mail_list:
                    mail_list.append(res)
            results=re.findall(r'href="([^\"]+)"',html)
            for res in results:
                if res not in href_list:
                    res=re.sub(r"^/",url+"/",res)
                    href_list.append(res) 
        results= re.findall(r'(["\'][^\'"?\s]+\.([a-z][\w\d]{0,6}))["\'?/]',html)
        results=set(results)
        for res in results:
            if res[1] not in not_ext:
                if res[1] not in ext_dict:
                    print("res1 " +res[1])
                    ext_dict[res[1]]=1
                else:
                    ext_dict[res[1]]+=1

        if flg!=True:
            print('Список телефонів:')
            await bot.send_message(query['from'].id,'Список телефонів:')
            print(str(tel_list))
            await bot.send_message(query['from'].id,str(set(tel_list)))
            print('Список емейлів:')
            await bot.send_message(query['from'].id,'Список емейлів:')
            print(str(mail_list))
            await bot.send_message(query['from'].id,str(mail_list))
            print('Список соцмереж')
            
            for soc in soclist:
                print(soc)
                await bot.send_message(query['from'].id,soc)
        ci=0
        answer=''
        for ky,val in ext_dict.items():
            answer+=f"&lt;{ky} {val}&gt;"
            ci+=1
        print(answer)
        await bot.send_message(query['from'].id,answer)
        print(f"{answer}")
        print("#"*80)

        file_results.clear()
        for ext in file_lst:
            files=re.findall(r'"([^"?\s]+\.'+ext +')[?"/]',html)
            if files:
                for res in files:
                    video_url=res
                    video_url=re.sub(r"^/",url+"/",video_url)
                    if not re.match(r"^https?:",video_url):
                        video_url=re.sub(r"^",url+"/",video_url)
                    video_url=re.sub(r"\\/","/",video_url)
                    if video_url not in file_results:

                        if video_url not in file_results:
                            file_results.append(video_url)
                            print(video_url)
                print("#"*80)
        resultat='Список телефонів:'+str(tel_list)+'\n'+'Список емейлів:'+str(mail_list) + '\nСписок соцмере:'+str(soclist)
        resultat+='\n' + str(ext_dict)+'\n' + str(file_results)
        
        print(f"{addresses}")

    except:
        print( query.query) 

##############################################################
if __name__ == '__main__':
    print('@weirdurlbot запущен!')                                    # ЧТОБЫ БОТ РАБОТАЛ ВСЕГДА с выводом в начале вашего любого текста
executor.start_polling(dp)
##############################################################