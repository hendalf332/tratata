#!/usr/bin/python3
import os
import sys
import matplotlib.pyplot as plt
from multiprocessing import Pool,Process,Queue,Lock
import multiprocessing

def dirsearch(drive,filedict,dirdict,ttlsz):
    print("drive ",drive)
    print(dirdict)
    for root, dirs, files in os.walk(drive):
        for name in files:
            fname=os.path.join(root, name)
            print(fname)
            if os.path.isfile(fname):
                try:
                    sz=os.path.getsize(fname)
                    # print(fname,' ',str(sz))
                    dirdict[drive]+=sz
                    ttlsz['totalsize']+=sz
                except FileNotFoundError:
                    print(f"Cant find file {fname}")
                splittup=os.path.splitext(fname)
                ext=splittup[1][1:].lower()
                if ext=='':
                    ext='БезРозширень'
                    if ext not in filedict:
                        filedict[ext]=1
                    else:
                        filedict[ext]+=1
                if ext not in filedict:
                    filedict[ext]=1
                else:
                    filedict[ext]+=1
   
def main():
    multiprocessing.freeze_support()
    drive=input('Введіть ім\'я папки:')
    plt.title(f"FileStatistics {drive}")
    with multiprocessing.Manager() as manager: 
        filedict=manager.dict()
        dirdict=manager.dict()
        ttlsz=manager.dict()
        ttlsz['totalsize']=0
        if not os.path.exists(drive) or not os.path.isdir(drive):
            print('[-]Нажаль папки не існує чи вказаний шлях не є папкою')
            sys.exit(1)
        for name in os.listdir(drive):
            if os.path.isdir(f"{drive}\\{name}"):
                name=f"{drive}\{name}"
                if name not in dirdict:
                    print(name)
                    name=name.replace(chr(92)+chr(92),chr(92))
                    dirdict[name]=0
            elif os.path.isfile(f"{drive}\{name}"):
                fname=f"{drive}\{name}"
                if os.path.isfile(fname):
                    splittup=os.path.splitext(fname)
                    ext=splittup[1][1:].lower()
                    if ext=='':
                        ext='БезРозширень'
                        if ext not in filedict:
                            filedict[ext]=1
                        else:
                            filedict[ext]+=1
                    if ext not in filedict:
                        filedict[ext]=1
                    else:
                        filedict[ext]+=1
                
        print(dirdict)  
        pool=Pool(processes=len(dirdict.keys()))
        print(len(dirdict.keys()))
        print(list(dirdict.keys()))
        vls= [(drv,filedict,dirdict,ttlsz) for drv in list(dirdict.keys())]
        print(type(vls))
        print(vls)
        pool.starmap(dirsearch,vls)
            
        filedict = sorted(filedict.items(), key=lambda x:x[1],reverse=True)
        filedict = dict(filedict)
        stats=filedict.values()
        extensions=filedict.keys()
        plt.pie(stats,labels=extensions,radius=1.5)
        plt.legend()
        for item in filedict:
            print(f"{item} {filedict[item]}")
        plt.show()

        dirdict = sorted(dirdict.items(), key=lambda x:x[1],reverse=True)
        dirdict = dict(dirdict)
        stats=dirdict.values()
        extensions=dirdict.keys()
        plt.pie(stats,labels=extensions,radius=1.5)   
        plt.legend()
        plt.show()

if __name__=='__main__':
	main()