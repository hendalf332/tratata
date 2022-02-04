#!/usr/bin/env python
# -*- coding: utf8 -*-
from pytube import YouTube
from mega import Mega
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TPE1, APIC, TSSE
from mutagen.mp4 import (MP4, Atom, Atoms, MP4Tags, MP4Info, delete, MP4Cover,
                         MP4MetadataError, MP4FreeForm, error, AtomDataType,
                         AtomError, _item_sort_key)
import json
import mutagen
from PIL import Image
from PIL.ExifTags import TAGS

import asyncio
import logging
####################################
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State   
from aiogram.types import InputFile   
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import filters
######################################################################
 
######################
import weirdbot_keyboard        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ keyboard.py
import config
######################

#######################
from multiprocessing import Process,Queue, Value
import requests
import sys
import re
import os
import csv
import string
import urllib.parse
from time import sleep
from time import time
import random
import io

import secrets
from pathlib import Path
import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util import Counter
import binascii
import tempfile
import shutil

from os import getenv
from bs4 import BeautifulSoup
#######################
from aiogram.dispatcher import FSMContext                            ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters import Command                        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.contrib.fsm_storage.memory import MemoryStorage        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters.state import StatesGroup, State        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM

######################
from tenacity import retry, wait_exponential, retry_if_exception_type

from mega.errors import ValidationError, RequestError
from mega.crypto import (a32_to_base64, encrypt_key, base64_url_encode,
                     encrypt_attr, base64_to_a32, base64_url_decode,
                     decrypt_attr, a32_to_str, get_chunks, str_to_a32,
                     decrypt_key, mpi_to_int, stringhash, prepare_key, make_id,
                     makebyte, modular_inverse)

def sendmsg(bot_token,chtid,msgtext):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chtid,
        "text": msgtext,
    }
    requests.get(url, params=params)

def video_downloader_proc(dcnt,yt,video_type,fname,bot_token,cht_id,msg_id,data,downloadtitle,downloadcnt,m,thmbFname,langtxt,mime_type,filesize):
    global file_size
    global chtid
    global msgid
    chtid=cht_id
    msgid=msg_id
    downloadcnt=dcnt.value
    file_size=filesize
    msgtext='Не можем скачати відео'
    try:
        fname=video_type.download(filename=fname)
    except:
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chtid}&text={msgtext}") 
        return
    #########################################
    if data[downloadtitle]['starttime']!=None and data[downloadtitle]['endtime']!=None:
        print(data[downloadtitle]['starttime'])
        starttime=int(data[downloadtitle]['starttime'])
        endtime=int(data[downloadtitle]['endtime'])
        clip = VideoFileClip(fname)
        duration=float(clip.duration)
        if endtime>(duration+1):
            msgtext=f"Кінцеве значення більше довжини відео {duration}сек"
            requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chtid}&text={msgtext}")
            return
        if endtime>starttime and endtime<=duration:
            difftime=endtime-starttime
            print(f"{starttime=} {endtime=} {difftime=}")
            newFName=downloadtitle+"."+str(difftime)+".mp4"
            print(f"{fname=} {newFName=}")
            try:
                ffmpeg_extract_subclip(fname, starttime, endtime, targetname=newFName)
            except:
                msgtext=f"Нажаль це відео розрізати не вдається"
                requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chtid}&text={msgtext}") 
                del data[downloadtitle]
                return
            fname=newFName
            file_size=os.path.getsize(fname)
    if file_size>50000000:
        print("Відео велике зараз відправимо його на Мега і дамо вам посилання на скачування")
        thmb=open(thmbFname,"rb")
        msgtext=f"Відео велике зараз відправимо його на сторонній WEBSERVER і дамо вам посилання на скачування"
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chtid}&text={msgtext}") 
        title=str(yt.title)
        title=re.sub(r'["\'\|\/#]','',title)
        newFName=fname
        print(f"{newFName=}")
        try:
            if mime_type=='mp4':
                audio = MP4(newFName)
                res=re.search(r'([^-]+)\s*-\s*([^\-]+)',yt.title)
                if res:
                    artist=res[1]
                    name=res[2]
                else:
                    name=yt.title
                    artist=yt.author
                audio["\xa9nam"] = name
                audio["\xa9ART"]=artist
                audio["desc"]=yt.author + " " + yt.channel_url
                audio["\xa9alb"]=f"Скачано ботом tyoutube3"
                cover_format = 'MP4Cover.FORMAT_JPEG'
                albumart = MP4Cover(thmb.read(), imageformat=cover_format)
                if yt.title in metadata:
                    print("title in metadata:")
                    print(str(metadata[yt.title]))
                    for data in metadata[yt.title]:
                        print(str(metadata[yt.title]))
                        print(f"data {data}")
                        try:
                            audio[data]=metadata[yt.title][data]
                        except KeyError:
                            print('Нема такого ключа')
                thmb.close()
                if type=='audio':
                    audio['covr'] = [bytes(albumart)]
                thmb=open(thmbFname,"rb")
                audio.save(newFName)
                thmb.close()
        except:
            msgtext=f"{langtxt[lang]['vid']} {yt.title} {langtxt[lang]['err']}"
            requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chtid}&text={msgtext}") 
            global_download_flag=False
            thmb.close()
        # except:
            # await bot.send_message(call['from'].id,f"{langtxt[lang]['vid']} {yt.title} {langtxt[lang]['err']}")
        newfname=str(downloadcnt)+'.mp4'
        dfile=m.find(newfname)
        if dfile:
            print(f'Знайдено файл {newfname}')
            print((m.destroy(dfile[0])))
        else:
            print(f'Не Знайдено файл {newfname}')
        folder = m.find('videos', exclude_deleted=True)
        if folder:
            file=m.myupload(filename=newFName,dest_filename=newfname)
            link=m.get_upload_link(file)
        else:
            m.create_folder('videos')
            newfname=str(downloadcnt)+'.mp4'
            print((m.destroy(dfile[0])))
            file=m.myupload(filename=newFName,dest_filename=newfname)
            link=m.get_upload_link(file)
            file = m.find(fname)
            link=m.get_upload_link(newfname)
        file=m.find(fname)
        print(link)
        msgtext=f"Посилання на відео {yt.title} {link}"
        sendmsg(bot_token,chtid,msgtext)

    else:
        with open(fname, "rb") as file:
            thmb=open(thmbFname,"rb")
            try:
                if mime_type=='mp4':
                    audio = MP4(fname)
                    
                    res=re.search(r'([^-]+)\s*-\s*([^\-]+)',yt.title)
                    if res:
                        artist=res[1]
                        name=res[2]
                    else:
                        name=yt.title
                        artist=yt.author
                    audio["\xa9nam"] = name
                    audio["\xa9ART"]=artist
                    audio["desc"]=yt.author + " " + yt.channel_url
                    audio["\xa9alb"]=f"Скачано ботом tyoutube3"
                    cover_format = 'MP4Cover.FORMAT_JPEG'
                    albumart = MP4Cover(thmb.read(), imageformat=cover_format)
                    if type=='audio':
                        audio['covr'] = [bytes(albumart)]
                    if yt.title in metadata:
                        print("title in metadata:")
                        for data in metadata[yt.title]:
                            print(f"data {data}")
                            try:
                                audio[data]=metadata[downloadtitle][data]
                            except KeyError:
                                print('Нема такого ключа')                        
                    thmb.close()
                    thmb=open(thmbFname,"rb")
                    audio.save(fname)

            except:
                msgtext=f"{langtxt[lang]['vid']} {yt.title} {langtxt[lang]['err']}"
                requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chtid}&text={msgtext}") 
            thmb.close() 
            
            url=f"https://api.telegram.org/bot{bot_token}/sendVideo"
            files={'video': open(fname, 'rb'),'thumb':open(thmbFname,"rb")}
            data = {'chat_id' : chtid}
            r=requests.post(url,params=data,files=files)
            print(r.status_code, r.reason, r.content)
            os.remove(fname)
            os.remove(thmbFname)
            
import logging # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ
logger = logging.getLogger(__name__) 
class MyMega(Mega):
    def __init__(self, options=None):
        print('MyMega')
        Mega.__init__(self, options=None)
        
    def myupload(self, filename, dest=None, dest_filename=None):
        global chtid
        global msgid
        print("myupload:")
        # determine storage node
        if dest is None:
            # if none set, upload to cloud drive node
            if not hasattr(self, 'root_id'):
                self.get_files()
            dest = self.root_id

        # request upload url, call 'u' method
        with open(filename, 'rb') as input_file:
            file_size = os.path.getsize(filename)
            ul_url = self._api_request({'a': 'u', 's': file_size})['p']

            # generate random aes key (128) for file
            ul_key = [random.randint(0, 0xFFFFFFFF) for _ in range(6)]
            k_str = a32_to_str(ul_key[:4])
            count = Counter.new(
                128, initial_value=((ul_key[4] << 32) + ul_key[5]) << 64)
            aes = AES.new(k_str, AES.MODE_CTR, counter=count)

            upload_progress = 0
            completion_file_handle = None

            mac_str = '\0' * 16
            mac_encryptor = AES.new(k_str, AES.MODE_CBC,
                                    mac_str.encode("utf8"))
            iv_str = a32_to_str([ul_key[4], ul_key[5], ul_key[4], ul_key[5]])
            if file_size > 0:
                for chunk_start, chunk_size in get_chunks(file_size):
                    chunk = input_file.read(chunk_size)
                    upload_progress += len(chunk)
                    parse_message=f"{upload_progress=} {len(chunk)}"
                    print(f"{upload_progress=} {len(chunk)}")
  
                    encryptor = AES.new(k_str, AES.MODE_CBC, iv_str)
                    for i in range(0, len(chunk) - 16, 16):
                        block = chunk[i:i + 16]
                        encryptor.encrypt(block)

                    # fix for files under 16 bytes failing
                    if file_size > 16:
                        i += 16
                    else:
                        i = 0

                    block = chunk[i:i + 16]
                    if len(block) % 16:
                        block += makebyte('\0' * (16 - len(block) % 16))
                    mac_str = mac_encryptor.encrypt(encryptor.encrypt(block))

                    # encrypt file and upload
                    chunk = aes.encrypt(chunk)
                    output_file = requests.post(ul_url + "/" +
                                                str(chunk_start),
                                                data=chunk,
                                                timeout=self.timeout)
                    completion_file_handle = output_file.text
                    logger.info('%s of %s uploaded', upload_progress,
                                file_size)
                    percent=file_size/100
                    percent=upload_progress/percent
                    parse_message=f"Закачалося на вебсервер {str(int(percent))}% {str(upload_progress)} of {str(file_size)} "
                    requests.get(f"https://api.telegram.org/bot{bot_token}/editMessageText?chat_id={chtid}&message_id={msgid}&text={parse_message}") 

            else:
                output_file = requests.post(ul_url + "/0",
                                            data='',
                                            timeout=self.timeout)
                completion_file_handle = output_file.text

            logger.info('Chunks uploaded')
            logger.info('Setting attributes to complete upload')
            logger.info('Computing attributes')
            file_mac = str_to_a32(mac_str)

            # determine meta mac
            meta_mac = (file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3])

            dest_filename = dest_filename or os.path.basename(filename)
            attribs = {'n': dest_filename}

            encrypt_attribs = base64_url_encode(
                encrypt_attr(attribs, ul_key[:4]))
            key = [
                ul_key[0] ^ ul_key[4], ul_key[1] ^ ul_key[5],
                ul_key[2] ^ meta_mac[0], ul_key[3] ^ meta_mac[1], ul_key[4],
                ul_key[5], meta_mac[0], meta_mac[1]
            ]
            encrypted_key = a32_to_base64(encrypt_key(key, self.master_key))
            logger.info('Sending request to update attributes')
            # update attributes
            data = self._api_request({
                'a':
                'p',
                't':
                dest,
                'i':
                self.request_id,
                'n': [{
                    'h': completion_file_handle,
                    't': 0,
                    'a': encrypt_attribs,
                    'k': encrypted_key
                }]
            })
            logger.info('Upload complete')
            parse_message=f"Upload complete"
            requests.get(f"https://api.telegram.org/bot{bot_token}/editMessageText?chat_id={chtid}&message_id={msgid}&text={parse_message}") 
            return data


class meinfo(StatesGroup):
    metaedit = State()
    setTrackTitle= State()
    setAlbum=State()
    setArtist=State()
    setaART=State()
    setComposer=State()
    setYear=State()
    setComments=State()
    setDescription=State()
    setGrouping=State()
    setGenre=State()
    setLyrics=State()
    setrange=State()
    setminrange=State()
    setmaxrange=State()
    
    

bot_token = config.GETORIGINALURLBOTTOKEN

storage = MemoryStorage() # FOR FSM
bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot,storage=storage)
downloadcnt=0
LOGFILE='youtube.log'
cnt=0
starttime=0
endtime=0
global_download_flag=False
yt=None
videourl=''
downloadurl=''
downloadtitle=''
messdict={}
metadata={}
data={}
chtid=0
msgid=0
lang='🇺🇦'
langtxt={'🇺🇦':{'OK':'Все Добре','skach':"Вибачте хтось скачує Зачекайте будьласка",'zvuk':'Звук','vid':'Відео','err':'Шось пішло не так','bigvid1':'Відео велике зараз розіб\'ємо його на','bigvid2':" частин\nІ кожну частину відправимо окремо",'pt':'частина №','from':'з','correct':"Будь ласка введіть коректне посилання на youtube відео",'vn':'Номер відео ','img':'Картинка з відео ','pr':'скачано','qual':'Виберіть якість відео чи тип','hlpmsg':'Бот скачує youtube відео\n Якшо звук mp4 то скачає ще метаданні картинку Ім\'я виконавця\n/starttime - початковий час \n/endtime - кінцевий час якщо ви хочете скачати відео частково','cngmeta':'Змінити метаданні?','y':'Так','n':'Ні','metaedt':'Редагування метаданних'},
'🇬🇧':{'OK':'Everything is OK','skach':"Sorry Somebody download wait please",'zvuk':'Sound','vid':'Video','err':'Something went wrong','bigvid1':'The Video is too big now split it on ','bigvid2':" parts\nAnd each part will send separately ",'pt':'part №','from':'from ','correct':"Please send us correct youtube video link",'vn':'Videonumber','img':'Thumbnail url','pr':'downloaded','qual':'Choose video quality or type','hlpmsg':'The Bot downloads youtube videos','cngmeta':'Change metadata?','y':'Yes','n':'No','metaedt':'Metadata editing'},
'🇩🇪':{'OK':'Alles Gud','skach':"Es tut mir leid, dass jemand heruntergeladen wurde, bitte warten",'zvuk':'Klang','vid':'Video','err':'Etwas ist schief gelaufen','bigvid1':'Das Video ist zu groß, jetzt teilen Sie es auf ','bigvid2':" Teile\nUnd jedes Teil wird separat gesendet ",'pt':'part №','from':' aus ','correct':"Bitte senden Sie uns den korrekten YouTube-Videolink",'vn':'Videonumber','img':'Thumbnail url','pr':'heruntergeladen','qual':'Wählen Sie Videoqualität oder -typ','hlpmsg':'Der Bot lädt YouTube-Videos herunter','cngmeta':'Metadaten ändern?','y':'Ja','n':'Nein','metaedt':'Metadaten ändern'},
'🇷🇺':{'OK':'Все Хорошо','skach':"Извените ктото скачивает пожалуйста",'zvuk':'Звук','vid':'Видео','err':'Чтото пошло не так','bigvid1':'Видео большое сейчас разобъем на ','bigvid2':" частей\nИ каждую часть отправим отдельно",'pt':'часть №','from':'из','correct':"Пожалуйста введите правильную ссылку на youtube видео",'vn':'Номер видео ','img':'Картинка с видео ','pr':'скачано','qual':'Виберите качество видео или тип','hlpmsg':'Бот скачивает youtube видео','cngmeta':'Поменять метаданные?','y':'Да','n':'Нет','metaedt':'Редактирование метаданних'},
'🇫🇷':{'OK':'Tout est bon','skach':"Désolé, quelqu'un télécharge Veuillez patienter",'zvuk':'Sonner','vid':'Vidéo','err':'Quelque chose s\'est mal passé','bigvid1':'La vidéo est géniale maintenant décomposons-la','bigvid2':" pièces \n Et nous enverrons chaque pièce séparément",'pt':'partie №','from':'avec ','correct':"Veuillez entrer le lien correct vers la vidéo youtube",'vn':'Numéro de vidéo','img':'Image de la vidéo ','pr':'téléchargé','qual':'Sélectionnez la qualité ou le type de vidéo','hlpmsg':'Bot télécharge la vidéo youtube \n Si le son est mp4, télécharge plus d\'image de métadonnées Nom de l\'artiste','cngmeta':'Modifier les métadonnées?','y':'Donc','n':'Non','metaedt':'Modification des métadonnées'}
}

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
mega=MyMega()
m = mega.login(config.email, config.passwd)
details = m.get_user()
print(str(details))

hlpmsg="""Бот скачує youtube відео
"""

async def setMetaData(attr,val):
    global metadata
    global downloadtitle
    if downloadtitle in metadata:
        metadata[downloadtitle].update({attr:val})
    else:
        metadata[downloadtitle]={attr:val}


@dp.message_handler(state=meinfo.setTrackTitle)
async def setData(message: types.Message, state: FSMContext):
    await setMetaData('\xa9nam',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setAlbum)
async def setAlbum(message: types.Message, state: FSMContext):
    print("set album")
    await setMetaData('\xa9alb',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setArtist)
async def setArtist(message: types.Message, state: FSMContext):
    print("set artist")
    await setMetaData('\xa9ART',message.text)
    await meinfo.metaedit.set()

###########################

@dp.message_handler(state=meinfo.setaART)
async def setaART(message: types.Message, state: FSMContext):
    await setMetaData('aART',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setComposer)
async def setComposer(message: types.Message, state: FSMContext):
    await setMetaData('\xa9wrt',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setYear)
async def setYear(message: types.Message, state: FSMContext):
    await setMetaData('\xa9day',message.text)
    await meinfo.metaedit.set()
    
###############################

@dp.message_handler(state=meinfo.setComments)
async def setComments(message: types.Message, state: FSMContext):
    await setMetaData('\xa9cmt',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setDescription)
async def setDescription(message: types.Message, state: FSMContext):
    await setMetaData('desc',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setGrouping)
async def setGrouping(message: types.Message, state: FSMContext):
    await setMetaData('\xa9grp',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setGenre)
async def setGenre(message: types.Message, state: FSMContext):
    await setMetaData('\xa9gen',message.text)
    await meinfo.metaedit.set()
    
@dp.message_handler(state=meinfo.setLyrics)
async def setLyrics(message: types.Message, state: FSMContext):
    await setMetaData('\xa9lyr',message.text)
    await meinfo.metaedit.set()

@dp.message_handler(content_types=['text'],state=meinfo.metaedit)
async def edit_metadata(message: types.Message, state: FSMContext):
    global downloadtitle
    global metadata
    global langtxt
    global lang
    cmdmsg=message.text
    mymsg=cmdmsg.split(' ')
    print(f"{downloadtitle=} {cmdmsg=}")
    if cmdmsg=='TrackTitle':
        await message.answer('Введіть назву пісні:')
        await meinfo.setTrackTitle.set()
        return
    elif cmdmsg=='album':
        await message.answer('Введіть назву альбому:')
        await meinfo.setAlbum.set()
        return
    elif cmdmsg=='artist':
        await message.answer('Введіть назву виконавця:')
        await meinfo.setArtist.set()
        return
    if cmdmsg=='albumArtist':
        await message.answer('Введіть назву виконавця:')
        await meinfo.setaART.set()
        return
    elif cmdmsg=='composer':
        await message.answer('Введіть назву композитора:')
        await meinfo.setComposer.set()
        return 
    if cmdmsg=='year':
        await message.answer('Введіть рік видання:')
        await meinfo.setYear.set()
        return
    elif cmdmsg=='comment':
        await message.answer('Введіть додаткові коментарі:')
        await meinfo.setComments.set()
        return
    if cmdmsg=='description':
        await message.answer('Введіть описання треку:')
        await meinfo.setDescription.set()
        return
    elif cmdmsg=='grouping':
        await message.answer('Введіть групування:')
        await meinfo.setGrouping.set()
        return      
    if cmdmsg=='genre':
        await message.answer('Введіть жанр:')
        await meinfo.setGenre.set()
        return
    elif cmdmsg=='lyrics':
        await message.answer('Введіть текст аудіо:')
        await meinfo.setLyrics.set()
        return         
    elif message.text=='🔙Назад':
        await message.answer(f"Перейдіть до повідомлення з відео і кнопками і натисніть скачати",reply_markup=weirdbot_keyboard.start,parse_mode='Markdown')
        await state.finish()
    else:
        await message.answer('Введіть команду з кнопок клавіатури:',reply_markup=weirdbot_keyboard.metaedit,parse_mode='Markdown')
 


def progress_func(stream=0,chunk=None,bytes_remaining=0):
    global file_size
    global chtid
    global msgid
    global downloadtitle
    global messdict
    global lang
    global langtxt
    percent=(100*(file_size-bytes_remaining))/file_size
    print("{:00.0f}% скачано".format(percent))
    percent="{:00.0f}% ".format(percent)+langtxt[lang]['pr']
    parse_message=f"{percent} {langtxt[lang]['vid']} {downloadtitle} "#.format(percent,downloadtitle)
    open_tp="open_tp"
    print(f"{chtid=} {msgid=} {stream.default_filename}")
    fname=stream.default_filename
    if fname in messdict:
        newchatid=messdict[fname][0]
        newmessgid=messdict[fname][1]
        requests.get(f"https://api.telegram.org/bot{bot_token}/editMessageText?chat_id={newchatid}&message_id={newmessgid}&text={parse_message}") 
        if percent=="100% "+langtxt[lang]['pr']:
            messdict.pop(fname,None)
    else:
        requests.get(f"https://api.telegram.org/bot{bot_token}/editMessageText?chat_id={chtid}&message_id={msgid}&text={parse_message}") 
        messdict[fname]=[chtid,msgid]


async def complete_func(stream=None,file_path=None):
    global downloadcnt,lang,langtxt
    print(f'download complete {file_path}')
    downloadcnt=downloadcnt-1
    print(f"{downloadcnt=}")

@dp.message_handler(commands=['settime'], state=None)
async def settime(message):
    global lang,langtxt
    msg=message.text
    msglst=msg.split('-')
    if len(msglst)<2:
        return
        
    start=msglst[0].split(' ')    
    start=start[1]        
    message.text=f"/starttime {start}"
    await starttime(message)
    endtm=f"/endtime {msglst[1]}"
    message.text=endtm
    await endtime(message)


@dp.message_handler(commands=['help'], state=None)
async def help(message):
    global lang,langtxt
    #await bot.send_message(message.chat.id, hlpmsg)
    await message.answer(langtxt[lang]['hlpmsg'])
    
@dp.message_handler(commands=['restart'], state=None)
async def restart(message):
    await message.answer("restart - Перезавантаження")
    os.system('sh restart.sh')
    sys.exit(0)

@dp.message_handler(commands=['loglist'], state=None)
async def loglist(message):
    cmdlist=[]
    global LOGFILE
    global global_download_flag
    global_download_flag=False
    folder = m.find('logs')
    logfile = m.find(LOGFILE)
    m.download(logfile)
    if os.path.exists(LOGFILE):
        file = list(csv.reader(open(LOGFILE,encoding="utf-8"),delimiter=';'))
        for row in file:
            if row not in cmdlist:
                cmdlist.append(row)
        for el in cmdlist:
            await message.answer(el)
            
@dp.callback_query_handler(text_contains='🇬🇧')
@dp.callback_query_handler(text_contains='🇺🇦')
@dp.callback_query_handler(text_contains='🇩🇪')
@dp.callback_query_handler(text_contains='🇷🇺')
@dp.callback_query_handler(text_contains='🇫🇷')
async def langproc(call: types.CallbackQuery):
    langtext=call.data
    print(langtext)
    if langtext not in ['🇬🇧','🇺🇦','🇩🇪','🇫🇷','🇷🇺']:
        await bot.send_message(call['from'].id,'Sorry no such language')
        return
    global lang
    lang=langtext
    await bot.delete_message(call.message.chat.id,call.message.message_id)
    return


@dp.message_handler(commands=['starttime'], state=None)
async def starttime(message):
    global data
    global downloadtitle
    print('hello starttime')
    msg=message.text
    msglst=msg.split(' ')
    if len(msglst)<2:
        return
    starttime=msglst[1]
    res=re.search(r'(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?',starttime)
    if res:
        res1=[]
        for el in [res.group(1),res.group(2),res.group(3)]:
            if el!=None:
                res1.append(el)
        print(res1)
        if len(res1)==3:
            hours=int(res1[0])
            minutes=int(res1[1])
            seconds=int(res1[2])
        elif len(res1)==2:
            hours=0
            minutes=int(res1[0])
            seconds=int(res1[1])
        elif len(res1)==1:
            hours=0
            minutes=0
            seconds=int(res1[0])
        else:
            hours=0
            minutes=0
            seconds=0
        if minutes>60 or seconds>60 or hours>60:
            return
        starttime=seconds+minutes*60+60*60*hours
        try:
            if data[downloadtitle]!=None:
                print(f"{starttime=}")
                await message.answer(f"starttime {starttime}")
                data[downloadtitle].update({'starttime':starttime})
        except:
            await message.answer(f"Відео не вказано")

@dp.message_handler(commands=['endtime'], state=None)
async def endtime(message):
    global data
    global downloadtitle
    msg=message.text
    msglst=msg.split(' ')
    if len(msglst)<2:
        return
    endtime=msglst[1]
    res=re.search(r'(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?',endtime)
    if res:
        res1=[]
        for el in [res.group(1),res.group(2),res.group(3)]:
            if el!=None:
                res1.append(el)
        print(res1)
        if len(res1)==3:
            hours=int(res1[0])
            minutes=int(res1[1])
            seconds=int(res1[2])

        elif len(res1)==2:
            hours=0
            minutes=int(res1[0])
            seconds=int(res1[1])
        elif len(res1)==1:
            hours=0
            minutes=0
            seconds=int(res1[0])
        else:
            hours=0
            minutes=0
            seconds=0
        if minutes>60 or seconds>60 or hours>60:
            return
        endtime=seconds+minutes*60+60*60*hours
        try:
            print(f"{endtime=}")
            if data[downloadtitle]!=None:
                await message.answer(f"endtime {endtime}")        
                data[downloadtitle].update({'endtime':endtime})
                try:
                    diff=endtime- int(data[downloadtitle]['starttime'])
                    await message.answer(f"Відео буде довжиною {diff}секунд") 
                except:
                    pass
            else:
                await message.answer(f"Відео не вказано") 
        except:
            await message.answer(f"Відео не вказано") 
            
@dp.message_handler(commands=['start'], state=None)
async def welcome(message):

    uname="{0.first_name}_{0.last_name}_{0.username}".format(message.from_user)
    global lang
    try:
        me=await bot.get_me()
        uname=message.from_user.username
        print(me.first_name)
        print(uname)

        await message.answer(f"Вітаємо {message.from_user.first_name} ,!\n Я - {me.username}\n /help довідка", reply_markup=weirdbot_keyboard.start, parse_mode='Markdown')
        langlist=['🇬🇧','🇺🇦','🇩🇪','🇫🇷','🇮🇹','🇪🇸','🇷🇺']
        resbuttons=[]
        for lng in langlist:
            btntext=lng
            btn=types.InlineKeyboardButton(btntext, callback_data = btntext)
            resbuttons.append(btn)
        resChoose = types.InlineKeyboardMarkup(row_width=4)
        resChoose.add(*resbuttons)
        await message.answer(f"Choose your language:",reply_markup=resChoose, parse_mode='Markdown')
    except:
        print('[-]Щось не так')
        return

@dp.callback_query_handler(text_contains='audio/')
@dp.callback_query_handler(text_contains='video/mp4')
@dp.callback_query_handler(text_contains='metadata')
@dp.callback_query_handler(text_contains='videointerval')
async def btnproc(call: types.CallbackQuery,state=None):
    print("query_handler")
    global lang
    global langtext
    global global_download_flag
    global metadata
    global downloadtitle
    global chtid
    global msgid   
    global data
    msg=call.data
    videourl=call.message.text.split(' ')
    videourl=videourl[0]
    if downloadtitle not in data:
        data[downloadtitle]={'videourl':videourl,'starttime':None,'endtime':None}
    print(msg)
        
    if 'metadata' in msg:
        print('changing metadata')
        videourl=call.message.text.split(' ')
        videourl=videourl[0]
        print(videourl)
        await bot.send_message(call['from'].id,f"{videourl} {langtxt[lang]['metaedt']}",reply_markup=weirdbot_keyboard.metaedit,parse_mode='Markdown')
        global_download_flag=False
        chtid=call.message.chat.id
        msgid=call.message.message_id
        await meinfo.metaedit.set()
        return

    global_download_flag=True
    print(f"{msg=}")
    videoLst=msg.split(' ')
    if len(videoLst)==2:
        myres=videoLst[1].strip()
        mime_type=videoLst[0].split('/')
        mime_type=mime_type[1]
        type=msg.split('/')
        type=type[0]
        print(f"{myres=} {mime_type=} {type=}")
        videourl=call.message.text.split(' ')
        videourl=videourl[0]
        print(f"{videourl=}")
        global downloadcnt
        global LOGFILE
        # try:
        yt=YouTube(videourl,on_progress_callback=progress_func)
        uname="{0.id}_{0.first_name}_{0.last_name}_{0.username}".format(call['from'])

        downloadcnt=downloadcnt+1
        downloadcnt= downloadcnt % 8
        global cnt        
        ytitle=yt.title
        downloadtitle=yt.title
        if not ytitle:
            ytitle="videonumber "+str(cnt)
        print(f"Title: {ytitle}\nThumbnail url {yt.thumbnail_url}")
        if type!="audio":
            video_type=yt.streams.filter(progressive=True,resolution=myres,file_extension=mime_type).first()
        else:
            video_type=yt.streams.filter(only_audio=True,file_extension=mime_type).first()
        global file_size
        
        file_size=video_type.filesize

        print(f"{file_size=}")

        thmbFname="thumbsnail"+str(cnt%100)+".jpg"
        cnt+=1
        kartinkaUrl=yt.thumbnail_url
        thmbFname=re.sub(r'\s','',thmbFname)
        with open(thmbFname, 'wb') as handle:
            response = requests.get(kartinkaUrl, stream=True)
            hdrs=response.headers
            print(f"Content-Type {hdrs['Content-Type']}")
            if not response.ok:
                print("ok")
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        fname=yt.title + "." +mime_type
        fname=re.sub(r'["\'\|\/#]','',fname)

        downloadtitle=yt.title
        chtid=call.message.chat.id
        msgid=call.message.message_id
        print(str(call.message))
        dcnt = Value('i', downloadcnt)
        proc=Process(target=video_downloader_proc,args=(dcnt,yt,video_type,fname,bot_token,chtid,msgid,data,downloadtitle,downloadcnt,m,thmbFname,langtxt,mime_type,file_size,))
        proc.start()
        print('Стартував новий процесс')
        global_download_flag=False
            
        del data[downloadtitle]


        ##################################
        print('++++++Adding video to logs+++++')
        folder = m.find('logs')
        logfile = m.find(LOGFILE)
        m.download(logfile)
        folder = m.find('logs')
        file = m.find(LOGFILE)
        if file:
            print('[+]Видалення файлу')
            print(m.destroy(file[0]))
        else:
            print('[-]Не Знайшовся')
        with open(LOGFILE,"a",encoding="utf-8", newline='') as file:
                writer=csv.writer(file,delimiter=';')
                writer.writerow((
                uname,
                videourl,
                yt.title
                )) 
        file=m.upload(LOGFILE,folder[0])
        ####################################

@dp.message_handler(content_types=['text'], state=None)
async def get_message(message):
    global lang
    global langtext
    global global_download_flag
    global downloadtitle
    global data
    if message.chat.type == 'private':
        if message.text=='❓ Довідка':
            await bot.send_message(message.chat.id,langtxt[lang]['hlpmsg'])
            return
        if message.text=='🔙Назад':
            await message.answer(langtxt[lang]['correct'],reply_markup=weirdbot_keyboard.start,parse_mode='Markdown')
    if global_download_flag==True:
        await message.answer(langtxt[lang]['skach'])
        return
    videourl=message.text
    if videourl.startswith("https://youtu") or videourl.startswith("https://www.youtu") or videourl.startswith("https://m.youtu"):
        await message.answer(langtxt[lang]['OK'])
    else:
        await message.answer(langtxt[lang]['correct'])
        return
	
    # try:
    global yt
    yt=YouTube(videourl)
    global downloadcnt
    print(f"Title: {yt.title}\nThumbnail url {yt.thumbnail_url}")
    kartinkaUrl=yt.thumbnail_url
    streamLst=yt.streams.filter(progressive=True,file_extension='mp4')
    resbuttons=[]
    for i,strm in enumerate(streamLst,0):
        btntext=str(strm.mime_type) + ' ' +str(strm.resolution)
        print(str(strm.itag) + ' ' +str(strm.resolution))
        resbuttons.append(types.InlineKeyboardButton(btntext, callback_data = btntext))
    streamLst=yt.streams.filter(only_audio=True)
    for i,strm in enumerate(streamLst,0):
        btntext=str(strm.mime_type+f" {langtxt[lang]['zvuk']}")# + ' ' +str(strm.resolution)
        print(str(strm.itag))# + ' ' +str(strm.resolution))
        btn=types.InlineKeyboardButton(btntext, callback_data = btntext)
        if btn not in resbuttons:
            resbuttons.append(btn)
                  

    btntext=str(f"{langtxt[lang]['cngmeta']} metadata")
    btn=types.InlineKeyboardButton(btntext, callback_data = btntext)  
    resbuttons.append(btn)    
    

    downloadtitle=yt.title
    resChoose = types.InlineKeyboardMarkup(row_width=2)
    resChoose.add(*resbuttons)
    if downloadtitle not in data:   
        data[downloadtitle]={'videourl':videourl,'starttime':None,'endtime':None}
    await bot.send_message(message.chat.id,f"{videourl} Title: {yt.title}\n{langtxt[lang]['img']} {yt.thumbnail_url}\n{langtxt[lang]['qual']}\nЯкщо хочете скачати відео частвово можна задати діапазон часу\n/starttime - початкове значення\n/endtime - кінцеве значення часу\n/settime strttime-endtime",reply_markup=resChoose, parse_mode='HTML')
    
if __name__ == "__main__":
    # Запуск бота
    print('@YoutubeDownloaderBot запущен!')  
    executor.start_polling(dp, skip_updates=True)
	
