from PIL import ImageGrab
import multiprocessing as mp
from multiprocessing import Pipe, Process
from pynput import keyboard

from pynput.keyboard import Key, Controller
from pynput.keyboard import HotKey
from multiprocessing import Pipe, Process
import multiprocessing as mp
import pyperclip as pc
import requests
import socket
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
            print(url)
            sleep(0.2)
            prs(keyboardctl,'<shift>+<home>')   
            sleep(0.2)
            prs(keyboardctl,'<ctrl>+x')
            sleep(0.2)
            clipboard=pc.paste()
            if not clipboard[0] in list(r',.[]qwertyuiop[]asdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'):  
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
        
        except:
            print('exception')
            sys.exit()

def on_activate():
    global buf
    global pipe
    print('hotkey activated')
    pipe[0].send('activate')


def main():
    mp.freeze_support()
    global buf
    global pipe
    pipe = Pipe(duplex=True)
    p1 = Process(target=pressProc, args=(pipe[1],))
    p1.start()
    hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<alt>+1'),
    on_activate)
    def for_canonical(f):
        print('for_canonical')
        return lambda k: f(l.canonical(k))
    with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
        while True:
            sleep(0.5)
        # l.join()    
    	
if __name__ == '__main__':
	main()
