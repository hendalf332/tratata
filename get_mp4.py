#!/usr/bin/env python
import requests
import sys
import re
import colorama
from colorama import init, Fore, Back, Style
import os
from bs4 import BeautifulSoup
from typing import Set, Union, List, MutableMapping, Optional
import urllib3
from urllib.parse import urlparse, urlunparse, urljoin
lxmlflag=True
try:
    import lxml
    from lxml import etree
except ImportError:
    lxmlflag=False
# essential for Windows environment
init()
# all available foreground colors
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
# all available background colors
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
# brightness values
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]


def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)
    
def find_all(s, c):
     idx = s.find(c)
     res=[]
     while idx != -1:
         res.append(idx)
         idx = s.find(c, idx + 1)
     return res

class LINKOVOD:
    _Links = Set[str]
    file_links={}
    emails=set()
    tels=set()
    socnetlinks=set()
    _CURRENT_URL=''
    def __init__(self,url):
        self._CURRENT_URL=url
        
    def get_links(self,url,html)-> _Links:
        soup=BeautifulSoup(html,'html.parser')
        proto=urlparse(url).scheme
        def gen():
            for link in soup.find_all('a'):
                try:
                    href=link.get('href').strip()
                    if href and not href.startswith('#')  and not href.startswith(('javascript:', 'mailto:')):
                        if href.startswith('//'):
                            href=proto+href
                        else:
                            href=urljoin(url,href)
                        yield href
                except KeyError:
                    pass
                except AttributeError:
                    pass
        return set(gen())


    def get_info(self,link,file_lst=None):
        print_with_color(link, color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
        myurl=link
        if link.find('/',9)!=-1:
            myurl=link[:find_all(link,'/')[-1]]+'/'
        print(f"{myurl=}")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        
        proto=urlparse(link).scheme       
        try:
            res = requests.get(link,headers=headers,stream=True,timeout=20)
            res_hdrs=res.headers
            contType=res_hdrs['Content-Type']
            if not "text/html" in contType or res.status_code!=200:      
                raise TypeError()
        except:
            print('ХОСТ недосяжний!!!')
            return file_lst
        html = res.text
        soclist=[]
        ext_dict={}
        mail_list=[]
        tel_list=[]
        href_list=[]
        results=re.findall(r'href="([^\"]+)"',html)
        for res in results:
            if res not in href_list:
                res=re.sub(r"^/",url+"/",res)
                href_list.append(res) 
        for soclnk in socnet_list:
            results=re.findall(r'(https?:\\?/\\?/(?:w{3}\.)?'+ soclnk +r'\\?/[^\s<\"\']+)[\s<\"\']',html)
            for res in results:
                if res not in soclist:
                    soclist.append(res)
                    if len(res)<60:
                        res=res.replace('\/','/')
                        self.socnetlinks.add(res)
                    
        results=re.findall(r'(https?:[^"\'\s]+)["\s\']',html)
        for res in results:
            if res not in href_list:
                res=re.sub(r"^/",url+"/",res)
                href_list.append(res)         
                
        results=re.findall(r"\+?(\d{,2}(?:\(\d{3,4}\))[\s\-](?:\d{2,3}[\s\-]?)(?:\d{2,3}[\s\-]){1,3}\d{2,3})[\s<\"\']",html)
        for res in results:
            if res not in tel_list:
                tel_list.append(res)
                self.tels.add(res)
                
        results=re.findall(r"\+\d{10,15}",html)
        for res in results:
            if res not in tel_list:
                tel_list.append(res)
                self.tels.add(res)
                #print(res)
        results=re.findall(r"([a-zA-Z0-9+_.-]+@(?:[a-zA-Z][a-zA-Z0-9-]+\.)+[a-zA-Z]+)",html)
        for res in results:
            if res not in mail_list:
                mail_list.append(res)
                self.emails.add(res)
                #print(res)
        if len(tel_list)>0:
            print('Список телефонів:')
            print(tel_list)
        if len(mail_list)>0:
            print('Список емейлів:')
            print(mail_list)
        if len(soclist)>0:    
            print('Список соцмереж:')
            for soc in soclist:
                print(soc)
        results=re.findall(r'"[^"?\s]+\.([\w\d]{1,7})["?/]',html)
        for res in results:
            if res not in not_ext:
                if res not in ext_dict:
                    ext_dict[res]=1
                    if not res in self.file_links.keys():
                        self.file_links[res]=set()
                else:
                    ext_dict[res]+=1
        ci=0
        for ky,val in ext_dict.items():
            print("<"+ky,f" {val}>",end='')
            ci+=1
            if ci%5==0:
                print()
        print("\n")#,"#"*80)
        if not file_lst:
            file_lst=list(map(str, input("Введіть список типів файлів для пошуку:").lower().split()))
        for ext in file_lst:
            files=re.findall(r'"([^"?\s]+\.'+ext +')[?"/]',html)
            if files:
                for res in files:
                    video_url=res
                    video_url=video_url.replace('\/','/')
                    if video_url.startswith('//'):
                        video_url=proto+video_url
                    else:
                        video_url=urljoin(link,video_url)
                        
                    if video_url not in results:

                        if video_url not in results:
                            results.append(video_url)
                            self.file_links[ext].add(video_url)
                # print("#"*80)
        return file_lst
        
    def printFileLinks(self):
        if lxmlflag==True: 
            root = etree.Element("root")
            files=etree.SubElement(root, "files")
            extfiles=etree.SubElement(root, "external.files")
            telephones=etree.SubElement(root, "telephones")
            emailtag=etree.SubElement(root, "emails")
            socnets=etree.SubElement(root, "socnets")
        chldlst={}
        extlst={}
        fl=open('res.txt','w',encoding='utf-8')
        for ky in self.file_links.keys():
            if len(self.file_links[ky])>0:
                if not ky in chldlst:
                    if lxmlflag==True: chldlst[ky]=etree.SubElement(files, ky)
                    if lxmlflag==True: extlst[ky]=etree.SubElement(extfiles, ky)
                for item in self.file_links[ky]:
                    print_with_color(f"{ky}:", color=Fore.MAGENTA, brightness=Style.BRIGHT,end='')
                    curhost=urlparse(self._CURRENT_URL).netloc
                    itemhost=urlparse(item).netloc
                    if curhost==itemhost:
                        if lxmlflag==True: chldlst[ky].append(etree.Element("a",href=item))
                    else:
                        if lxmlflag==True: extlst[ky].append(etree.Element("a",href=item))
                    print(f'{item}')
                    fl.write(f'{ky}:{item}\n')
        print('Показати емейли')
        fl.write(f'\nСписок емейлів:\n')
        for mail in self.emails:
            print(mail)
            fl.write(f'{mail}\n')
            if lxmlflag==True: emailtag.append(etree.Element("mail",email=mail))
        fl.write(f'\nСписок телефонів:\n')
        print('Показати телефони')
        for tel in self.tels:
            print(tel) 
            if lxmlflag==True: telephones.append(etree.Element("tel",number=tel))
            fl.write(f'{tel}\n')
        fl.write(f'\nСписок посилань на соцмережі:\n')
        print('Показати посилання на соцмережі:')
        for soc in self.socnetlinks:
            print(soc)
            if lxmlflag==True: socnets.append(etree.Element("socnet",link=soc))
            fl.write(f'{soc}\n')
        fl.close()
        if lxmlflag==True:
            myxml=etree.tostring(root, pretty_print=True)
            with open("res.xml",'w',encoding='utf-8') as fl:            
                fl.write(myxml.decode('utf-8'))
        return        

if os.name=='nt':
    colorama.init(convert=True)
     
cnt=0
file_lst=[]
href_list=[]
not_ext=[]
socnet_list=('facebook.com','vk.com','vm.tiktok.com','instagram.com','odnoklassniki.ru','ok.ru','youtube.com','tiktok.com','t.me')
weblinks=('com','net','org','ru','us','ua','edu','it','de','bg','nl','fr','at','es','hu')
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
        mylinks=LINKOVOD(link)
        lnks= mylinks.get_links(link,html)
        fllst=None
        for lnk in lnks:
            print(f"lnk {lnk}")
            fllst=mylinks.get_info(lnk,fllst)
        mylinks.printFileLinks()
        try:
            os.startfile('res.txt')
            print_with_color(f"[+]Results are in files res.txt & res.xml", color=Fore.WHITE, brightness=Style.BRIGHT)
        except:
            print('[-]Не можу відкрити файл!!!')
    cnt+=1
input()
