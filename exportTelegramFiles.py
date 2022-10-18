import json
import os
import glob
import shutil
from pathlib import Path
concatDict={}
def moveFile(src,dst):
    try:
        shutil.move(src,dst)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)
def concatFiles():
    print(concatDict)
    for file,partItem in concatDict.items():
        with open(file,'wb') as fw:
            for itemFl in partItem:
                try:
                    with open(itemFl,'rb') as fr:
                        buf=fr.read()
                        fw.write(buf)
                    os.remove(itemFl)
                except FileNotFoundError:
                    print(f"FileNotFoundException {itemFl}")
        
 
def main():
    myp=Path(__file__)
    cwd=myp.cwd()
    if os.name=='nt':
        sep='\\'
        jsfile=glob.glob(os.environ['USERPROFILE']+'\\Downloads\\Telegram Desktop\\ChatExport*\\result.json')
    else:
        sep='/'
        uname=os.popen('uname -a')
        if 'Android' in uname:
            jsfile=glob.glob('/sdcard/Telegram/ChatExport*/result.json')[-1]
    for cnt,jsfl in enumerate(jsfile):
        print(cnt+1,'>',jsfl)
    typef=input("FILES чи VIDEOFILES:")
    fnum=int(input('Введіть номер файлу для експорту:'))
    jsfile=jsfile[fnum-1]
    head=os.path.split(jsfile)[0]
    
    with open(jsfile,'r',encoding='utf-8') as fl:
        jsfl=json.load(fl)
    print(type(jsfl))
    msgs=jsfl['messages']
    print(type(msgs))
    for msg in msgs:
        print(msg['file'])
        if type(msg['text'])==type([]):
            info = msg['text'][0].split('|')
            origfname=msg['text'][-1]
        else:    
            info=msg['text'].split('|')
            origfname=info[-1]
        folder=info[0].split(':')[1]
        host=info[1].split(':')[1]
        origfname=info[2].split(':')[1]
        
        if not os.path.exists(host):
            os.mkdir(host)
        if not os.path.exists(f"{host}{sep}{folder}"):
            os.mkdir(f"{host}{sep}{folder}")
        print(f'folder {folder} Host:{host}')
        oldFileName=f"{head}{sep}{msg['file']}"
        try:
            fileName=info[3]
        except IndexError:
            fileName=origfname
        newFileName=f"{sep}{host}{sep}{folder}{sep}{fileName}"
        if os.name=='nt':
            oldFileName=oldFileName.replace('/','\\')
        origFName=f".{sep}{host}{sep}{folder}{sep}{origfname}"
        print(f"{origFName=}{newFileName=}")
        if origfname!=fileName:
            if not origFName in concatDict:
                concatDict[origFName]=[f".{sep}{host}{sep}{folder}{sep}{fileName}"]
            else:
                concatDict[origFName].append(f".{sep}{host}{sep}{folder}{sep}{fileName}")
            print(f"{head}{sep}{typef}{sep}{fileName} +",f"{cwd}{newFileName}")
            moveFile(f"{head}{sep}{typef}{sep}{fileName}",f"{cwd}{newFileName}")
        else:
            if os.name=='nt':
                newFileName=newFileName.replace('/','\\')
            print(f"moveFile({oldFileName},{newFileName})")
            moveFile(oldFileName,f"{cwd}{newFileName}")
    concatFiles()

if __name__ == '__main__':
	main()