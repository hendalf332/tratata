#!/usr/bin/python
# -*- coding: utf-8 -*-
import win32gui
from ctypes import windll
import win32api as api, win32process as proc
import cv2
import os
import re
from tkinter import *
#import tkinter as tk
from PIL import Image, ImageTk
import sys
# from pynput import keyboard

from pynput.keyboard import Key, Controller
from pynput.keyboard import HotKey
keyboardctl=Controller()
mypid=os.getpid()

def mykill(name):
    PROCESS_TERMINATE = 1
    Data = list(os.popen('wmic process get processid,commandLine'))
    for item in Data:
        try:
            item=item.split()
            pid=item[-1]
            cmdLine=" ".join(item[:-1])
            if name in cmdLine:
                pid=int(pid)
                if pid!=mypid:
	                print(f"name={name}")
	                handle = windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
	                windll.kernel32.TerminateProcess(handle, -1)
	                windll.kernel32.CloseHandle(handle)
                
        except IndexError:
            pass
    return


scriptname=sys.argv[0]
myname=scriptname.split('\\')[-1]
print(f"{myname=}")
mykill(myname)
try:
	if sys.argv[1]:
		imgpth=sys.argv[1]
		if not "\\\\" in imgpth:
			imgpth=imgpth.replace("\\","\\\\")
		print(imgpth)
		if imgpth.lower().endswith('jpg') or imgpth.lower().endswith('jpeg') or imgpth.lower().endswith('png') and os.path.exists(imgpth):
			with open(scriptname,'r',encoding='utf-8',newline='') as fl:
				myscript=fl.read()
				newscript=re.sub(r"(\s+)imgpth=r'([^']*)'","\\1imgpth=r'"+imgpth+"'",myscript)
				print(newscript)
			with open(scriptname,'w',encoding='utf-8',newline='') as fl:
				fl.write(newscript)


except:
	imgpth=r'D:\Users\tonnyr2\Pictures\btn3.png'

def prs(ctrlr:Controller,keys:str):
    keys=HotKey.parse(keys)
    for it in keys:
        ctrlr.press(it)
    for it in keys[::-1]:
        ctrlr.release(it)

def onclick():
	prs(keyboardctl,'<ctrl>+<esc>')

window = Tk()  #Makes main window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
print(f"screendimensions {screen_width}x{screen_height}")

window.overrideredirect(True)
window.wm_attributes("-topmost", True)
x,y,w,h=2,2,40,22
window.geometry("+600+200")
display1 = Button(window,command=onclick)
display1.grid(row=1, column=0, padx=0, pady=0)  #Display 1

def callback(hwnd, extra):
	global window,w,h
	if win32gui.IsWindowVisible(hwnd):
		txt=win32gui.GetWindowText(hwnd)
		# print(f"window text: '{win32gui.GetWindowText(hwnd)}'")
		if txt=="Start" or txt=="Пуск":
			rect=win32gui.GetWindowRect(hwnd)
			x = rect[0]
			y = rect[1]
			w = rect[2] - x 
			h = rect[3] - y
			# print(f"Coords:{x} {y} dimensions:{w}x{h}")
			window.geometry(f"{w}x{h}+{x}+{y}")

def show_frame():
	win32gui.EnumWindows(callback, None)
	img=cv2.imread(imgpth)
	cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
	cv2image = cv2.resize(cv2image, dsize=(w,h), interpolation=cv2.INTER_CUBIC)
	img = Image.fromarray(cv2image)
	imgtk = ImageTk.PhotoImage(master = display1, image=img)
	display1.imgtk = imgtk #Shows frame for display 1
	display1.configure(image=imgtk)	
	window.overrideredirect(True)
	window.wm_attributes("-topmost", True)	
	window.after(1, show_frame)
show_frame()
window.mainloop()
