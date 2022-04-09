import re
import subprocess
import os
import glob
import time
import socket
import shutil
import config
from pyfiglet import Figlet
import sys

def main():
    preview_text=Figlet(font='slant')
    print(preview_text.renderText('WLAN SETUP'))
    complist=glob.glob('.\wilog_*.log')
    for idx,comp in enumerate(complist):
        complist[idx]=complist[idx][len('.\wilog_'):]
        complist[idx]=complist[idx][:complist[idx][::-1].index('.')*(-1)-1]
        
    compname=input(f"введіть ім'я компу зі списку {complist}:")
    fname=f'wilog_{compname}.log'
    if not os.path.exists(fname):
        print('[-] Файлу не існує')
        return
    widict={}
    with open(fname ,'r+', encoding='utf-8') as wifier:
        lines=wifier.readlines()
        for line in lines:
            data=list(line.split(' '))
            passwd=data[-1].strip()
            essid=list(data[-2].split(':'))[-1].strip()
            
            print(essid,' ',passwd)
            hx=''
            for ch in essid:
                hx+=hex(ord(ch))[2:]
            profile=f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
	<name>{essid}</name>
	<SSIDConfig>
		<SSID>
			<hex>{hx}</hex>
			<name>{essid}</name>
		</SSID>
	</SSIDConfig>
	<connectionType>ESS</connectionType>
	<connectionMode>auto</connectionMode>
	<MSM>
		<security>
			<authEncryption>
				<authentication>WPA2PSK</authentication>
				<encryption>AES</encryption>
				<useOneX>false</useOneX>
			</authEncryption>
			<sharedKey>
				<keyType>passPhrase</keyType>
				<protected>false</protected>
				<keyMaterial>{passwd}</keyMaterial>
			</sharedKey>
		</security>
	</MSM>
</WLANProfile>
            """
            # with open(f".\wlan0-{essid}.xml",'w') as pr:
                # pr.write(profile)
            os.popen(f'netsh wlan add profile filename=".\wlan0-{essid}.xml"')
		
if __name__=='__main__':
    main()