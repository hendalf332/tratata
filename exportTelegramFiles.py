import json
import os
import glob
import shutil

def moveFile(src,dst):
    try:
        shutil.move(src,dst)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)
        
def main():
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
    fnum=int(input('Введіть номер файлу для експорту:'))
    jsfile=jsfile[fnum-1]
    head=os.path.split(jsfile)[0]
    
    with open(jsfile,'r') as fl:
        jsfl=json.load(fl)
    print(type(jsfl))
    msgs=jsfl['messages']
    print(type(msgs))
    for msg in msgs:
        print(msg['file'])
        if type(msg['text'])==type([]):
            info = msg['text'][0].split(' ')
            origfname=msg['text'][-1]
        else:    
            info=msg['text'].split(' ')
            origfname=info[-1]
        folder=info[0].split(':')[1]
        host=info[1].split(':')[1]
        origfname=info[2].split(':')[1]
        
        
        if not os.path.exists(host):
            os.mkdir(host)
        if not os.path.exists(f"{host}{sep}{folder}"):
            os.mkdir(f"{host}{sep}{folder}")
        print(f'folder {folder} Host:{host} \nOriginalFname:{origfname}')
        oldFileName=f"{head}{sep}{msg['file']}"
        if os.name=='nt':
            oldFileName=oldFileName.replace('/','\\')
        newFileName=f".{sep}{host}{sep}{folder}{sep}{origfname}"

        if os.name=='nt':
            newFileName=newFileName.replace('/','\\')
        print(f"moveFile({oldFileName},{newFileName})")
        moveFile(oldFileName,newFileName)

if __name__ == '__main__':
	main()
