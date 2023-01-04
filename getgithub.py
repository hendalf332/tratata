#!/usr/bin/env python
import requests
import re
import os,sys
import colorama
import readchar
from colorama import init, Fore, Back, Style

sep='/'
if os.name == 'nt':
	sep='\\'
else:
	sep='/'

folder_list=[]
mainFolders=[]
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

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


URL='https://github.com/edoardottt/black-hat-python3-code'#'https://github'
URL='https://github.com/monoxgas/sRDI'
URL='https://github.com/Priler/samurai'
URL='https://github.com/hendalf332/tratata'
URL='https://github.com/hendalf332/hendalf332.github.io'
URL='https://github.com/codingforentrepreneurs/OpenCV-Python-Series'
HEADERS={'user-agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36','accept':'*/*'}

def get_html(url,useragent=None,proxy=None):
    r=requests.get(url,headers=useragent,proxies=proxy)
    return r

def print_links(links,selected):
	clr()
	global folder_list
	global mainFolders

	for idx,link in enumerate(links,start=1):
		ln=39-len(str(idx))
		if link[1]!=URL:
			link=link[1].split("/")[-1]+'/'+link[0].split("/")[-1]
		else:
			link=link[0].split("/")[-1]
		if idx % 3 >0:
			if idx in selected:
				print_with_color(f"{idx}> {link:<{ln}}",end='', color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
			else:
				print(f"{idx}> {link:<{ln}}",end=' ')
		else:
			if idx in selected:
				print_with_color(f"{idx}> {link:<{ln}}", color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
			else:
				print(f"{idx}> {link:<{ln}}")
	print('\nMainFolderList:')
	for idx,link in enumerate(mainFolders,start=idx+1):
		ln=39-len(str(idx))
		if link==URL:
			idx-=1
			continue
		link=link.split("/")[-1]
		if idx % 3 >0:
			if idx in selected:
				print_with_color(f"{idx}> {link:<{ln}}",end='', color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
			else:
				print(f"{idx}> {link:<{ln}}",end=' ')
		else:
			if idx in selected:
				print_with_color(f"{idx}> {link:<{ln}}", color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
			else:
				print(f"{idx}> {link:<{ln}}")
	print('\nAllFolderList:')
	for idx,link in enumerate(folder_list,start=idx+1):
		ln=39-len(str(idx))
		if link==URL:
			idx-=1
			continue
		link=link.split("/")[-1]
		if idx % 3 >0:
			if idx in selected:
				print_with_color(f"{idx}> {link:<{ln}}",end='', color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
			else:
				print(f"{idx}> {link:<{ln}}",end=' ')
		else:
			if idx in selected:
				print_with_color(f"{idx}> {link:<{ln}}", color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
			else:
				print(f"{idx}> {link:<{ln}}")	
	print()			

def get_details(html,folder):
    mylinks=[]
    results=re.findall(r"href=\"(\/[^\"]+\/blob\/(?<!tree)[a-zA-Z]+\/.+)\"",html)
    for res in results:

    	res='https://raw.githubusercontent.com'+res
    	if not (res,folder) in mylinks:
    		mylinks.append((res,folder))
    return mylinks
def downloadDir(dirname):
	print(f'Скачаємо папку: {dirname}')
	dirlist=[dirname]
	global folder_list
	if not os.path.exists(dirname.split('/')[-1]) or not os.path.isdir(dirname.split('/')[-1]):
		os.mkdir(dirname.split('/')[-1])
	for folder in folder_list:
		if folder.startswith(dirname) and folder!=dirname:
			print(f"subfolder: {folder}")
			mypath=f".\\{dirname.split('/')[-1]}\\{folder.split('/')[-1]}"
			if not os.path.exists(mypath) or not os.path.isdir(mypath):
				os.mkdir(mypath)
			dirlist.append(folder)
			print(folder.split('/')[-1])
	for dr in dirlist:
		html=get_html(dr,useragent=HEADERS)
		links=[]
		if html.status_code==200:
			links=get_details(html.text,dr)
			for link in links:
				link=link[0]
				link=link.replace('/blob/','/')
				res=get_html(link,useragent=HEADERS)
				if res.status_code==200:
					scriptText=res.text
					print(link)
					if dirname.split('/')[-1]!=dr.split('/')[-1]:
						path=f".{sep}{dirname.split('/')[-1]}{sep}{dr.split('/')[-1]}{sep}{link.split('/')[-1]}"
					else:
						path=f".{sep}{dr.split('/')[-1]}{sep}{link.split('/')[-1]}"
					with open(path,'w',encoding="utf-8") as fl:
					 	fl.write(scriptText)


def get_folders(html,parent):
	folderList=[]
	global folder_list
	global mainFolders

	results=re.findall(r"href=\"([^\"]+\/tree\/[a-zA-Z]+\/.+)\"",html)
	for res in results:
		if not res.startswith('https://github.com'):
			res='https://github.com'+res
			folderList.append(res)
			if parent==URL:
				mainFolders.append(res)
	for res in folderList:
		html=get_html(res,useragent=HEADERS)
		if html.status_code==200:
			if res not in folder_list:
				folder_list.append(res)
				folders=get_folders(html.text,res)
	return folder_list

def main():
		global folder_list
		try:
			html=get_html(URL,useragent=HEADERS)
		except:
			print('error')
		links=list()
		selected=[]
		if html.status_code==200:
			folderlist=get_folders(html.text,URL)
			folderlist.append(URL)
			for folder in folderlist:
				fdr=folder
				folder=get_html(folder,useragent=HEADERS)
				links.extend(get_details(folder.text,fdr))			
			#links.extend(mainFolders)
			print(len(links))
			while 1:
				if len(links):
					links=sorted(links,key=lambda x: x[0])
					print_links(links,selected)
					idx=int(input('Enter script index: '))
					selected.append(idx)
					print_links(links,selected)
					if idx<=len(links):
						myscriptlink=links[idx-1][0]
						myscriptlink=myscriptlink.replace('/blob/','/')
						print(myscriptlink)
						res=get_html(myscriptlink,useragent=HEADERS)
						if res.status_code==200:
							scriptText=res.text
							scripFName=myscriptlink.split("/")[-1]
							with open(scripFName,'w',encoding="utf-8") as fl:
								fl.write(scriptText)
							if scripFName.endswith('.py'):
								print(f'Чи запустити/читати на виконання файл {scripFName} (y/r/n)?',end='')
								ch=readchar.readchar()
								try:
									ans=str(ch,encoding='UTF-8').lower()
								except:
									ans=ch.lower()
								if ans=='y':
									os.system(f"python {scripFName}")
								elif ans=='r':
									os.system(f"more {scripFName}")
								print()
							else:
								print(f'Прочитати файл {scripFName} (y/n)?',end='')
								ch=readchar.readchar()	
								try:
									ans=str(ch,encoding='UTF-8').lower()
								except:
									ans=ch.lower()
								if ans=='y':
									os.system(f"more {scripFName}")
								print()
					elif idx<(len(links)+len(mainFolders)+1):
						idx=idx-len(links)
						downloadDir(mainFolders[idx-1])
					else:
						idx=idx-(len(links)+len(mainFolders))
						downloadDir(folder_list[idx-1])						

					try:
						print('Press ANYKEY to continue or q to quit....',end='')
						ch=readchar.readchar()
						try:
							ans=str(ch,encoding='UTF-8').lower()
						except:
							ans=ch.lower()
						if ans=='q':
							sys.exit(0)
					except UnicodeDecodeError:
						pass
					print()

if __name__ == '__main__':
	main()