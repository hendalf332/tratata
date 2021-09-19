#!/usr/bin/env python
import csv
import os
import re
import lxml
import sys
import requests
from bs4 import BeautifulSoup
################
import pytesseract
from PIL import Image, ImageEnhance

URL='https://www.vpnbook.com/freevpn'
HEADERS={'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36','accept':'*/*'}
PASSFILE=r'password.png'
def get_html(url,headers):
    r=requests.get(url,headers=headers,stream=True,timeout=10)
    return r
	
def main():

    html=get_html(URL,HEADERS)
    if html.status_code==200:
        html=html.text
        soup=BeautifulSoup(html,'lxml')
        try:
            img=soup.find("img",src=re.compile("password")).get("src").strip()
            uname=soup.find("img",src=re.compile("password")).find_previous('strong').text.strip()
            print(uname)
        except:
            pass
        if img:
            img='https://www.vpnbook.com/'+img
            print(img)
            print(f"Username: {uname}")
            img_data = requests.get(img).content
            with open(PASSFILE, 'wb') as handler:
                handler.write(img_data)
            try:
                passimg=Image.open(PASSFILE,mode='r')
                #print("Размер изображения:")  
                #print(passimg.format, passimg.size, passimg.mode)
                
                passimg = passimg.convert(mode="RGB")
                sz=passimg.size
                width=int(sz[0])
                height=int(sz[1])
                contrast = ImageEnhance.Contrast(passimg)
                im_output = contrast.enhance(1000)
                maxsize=1.09
                newsize = (int(round(maxsize * width)), int(round( height)))
                im_output = im_output.resize(newsize)
                passimg.show()
                im_output.show()
            except FileNotFoundError:  
                print("Файл не найден")
                sys.exit(1)

            pytesseract.pytesseract.tesseract_cmd=r'd:\Users\tonnyr2\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
            custom_config=r'--oem 3 --psm 1'
            pwd=pytesseract.image_to_string(im_output,config=custom_config).strip()
            
            print(f"Пароль: {pwd}")
            # os.startfile(PASSFILE)
            with open('pass.txt','w') as passtxt:
                passtxt.write(pwd)
            input()
if __name__=='__main__':
	main()
