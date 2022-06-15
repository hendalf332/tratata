import multiprocessing as mp
from multiprocessing import Pipe, Process
from pynput import keyboard

from pynput.keyboard import Key, Controller
from pynput.keyboard import HotKey
from multiprocessing import Pipe, Process
import multiprocessing as mp
import pyperclip as pc
import requests
import sys
import io
from time import sleep
import re
buf=''
def prs(ctrlr:Controller,keys:str):
    keys=HotKey.parse(keys)
    for it in keys:
        ctrlr.press(it)
    for it in keys[::-1]:
        ctrlr.release(it)
        
def pressProc(pipe:mp.Pipe):
    print("[+]pressProc Activated")
    keyboardctl=Controller()
    while True:
        try:
            url = pipe.recv()
            clipbackup=pc.paste()
            print(url)
            sleep(0.2)
            if url=='all':
                prs(keyboardctl,'<shift>+<home>')   
                sleep(0.2)
            prs(keyboardctl,'<ctrl>+x')
            sleep(0.2)
            clipboard=pc.paste()
            if not clipboard[0] in list(r';\',.[]qwertyuiop[]asdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'):  
                print('yes')
                translation = str.maketrans(dict(zip('"йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ.',"@qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./")))
            else:
                print('no')
                translation = str.maketrans(dict(zip("@qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./",'"йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ.')))

            clipboard = clipboard.translate(translation) 
            buf=clipboard
            pc.copy(clipboard)
            sleep(0.2)
            pc.paste()
            prs(keyboardctl,'<ctrl>+v')
            sleep(0.1)
            prs(keyboardctl,'<alt>+<shift>')
            pc.copy(clipbackup)
        
        except:
            print('exception')
            sys.exit()

def on_activate():
    global buf
    global pipe
    print('hotkey activated1')
    pipe[0].send('all')
    
def on_activate2():
    global buf
    global pipe
    print('hotkey activated2')
    pipe[0].send('selected')    


def main():
    mp.freeze_support()
    print('<alt+1> -- Change layout in all string\n<alt>+` - Change selected text layout')
    global buf
    global pipe
    pipe = Pipe(duplex=True)
    p1 = Process(target=pressProc, args=(pipe[1],))
    p1.start()
    hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<alt>+1'),
    on_activate)
    hotkey2=keyboard.HotKey(
    keyboard.HotKey.parse('<alt>+`'),
    on_activate2)
    def for_canonical(f):
        print('for_canonical')
        return lambda k: f(l.canonical(k))
    with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
        with keyboard.Listener(
            on_press=for_canonical(hotkey2.press),
            on_release=for_canonical(hotkey2.release)) as l2:        
            while True:
                sleep(0.5)
        # l.join()    
    	
if __name__ == '__main__':
	main()
