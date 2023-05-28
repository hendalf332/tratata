import numpy as np
import cv2
import os
import math
import win32process
import win32process as process
import win32gui
import win32con
import time
from tkinter import *
from PIL import Image, ImageTk
from pynput.mouse import Button, Controller
mouse = Controller()


mypid=os.getpid()
print(f"{mypid=}")
x,y=0,0
mouse_x,mouse_y=0,0
pmouse_x,pmouse_y=0,0

window = Tk()  #Makes main window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
print(f"screendimensions {screen_width}x{screen_height}")

window.geometry("120x100+950+720")
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
display1 = Label(window)
display1.grid(row=1, column=0, padx=0, pady=0)  #Display 1
def show_frame():
	global pmouse_x,pmouse_y,mypid,mouse
	# window.overrideredirect(True)
	window.wm_attributes("-topmost", True)		
	try:
		mouse_x,mouse_y=mouse.position
	except TypeError:
		mouse_x,mouse_y=0,0
	# print(mouse_x,mouse_y)
	if mouse_x!=pmouse_x and mouse_y!=pmouse_y:
				# Difference in x coordinates
		show_window_by_process(mypid)
		dx = mouse_x - x
		# Difference in y coordinates
		dy =  mouse_y - y
		theta = math.atan2(dy, dx)
		center=25,31
		center2=80,31
		radius=9
		newpx=int(radius*math.cos(theta)+center[0])
		newpy=int(radius*math.sin(theta)+center[1])
		newpx2=int(radius*math.cos(theta)+center2[0])
		newpy2=int(radius*math.sin(theta)+center2[1])		
		newrad=7
		n_channels = 4
		img=np.zeros((52,57,n_channels),np.uint8)
		circle_centerx,circle_centery=img.shape[:2]
		circle_centerx=int(circle_centerx/2)
		circle_centery=int(circle_centery/2)
		cv2.circle(img,(circle_centerx,circle_centery),20,(255,255,255),-1)
		img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		numpy_horizontal_concat = np.concatenate((img, img), axis=1)
		cv2.circle(numpy_horizontal_concat,(newpx,newpy),newrad,(0,0,0),-1)
		cv2.circle(numpy_horizontal_concat,(newpx2,newpy2),newrad,(0,0,0),-1)

		#cv2.imshow('xeyes', numpy_horizontal_concat)	

		cv2image = cv2.cvtColor(numpy_horizontal_concat, cv2.COLOR_BGR2RGBA)
		img = Image.fromarray(cv2image)
		imgtk = ImageTk.PhotoImage(master = display1, image=img)
		display1.imgtk = imgtk #Shows frame for display 1
		display1.configure(image=imgtk)

	window.after(1, show_frame)

	pmouse_x=mouse_x
	pmouse_y=mouse_y

def callbackSetWinPosition(hwnd, extra):
	global window,screen_height,screen_width,x,y
	txt=win32gui.GetWindowText(hwnd)
	# print(f"window text: '{win32gui.GetWindowText(hwnd)}'")
	if txt=="Start" or txt=="Пуск":
		rect=win32gui.GetWindowRect(hwnd)
		x = rect[0]
		y = rect[1]
		w = rect[2] - x
		h = rect[3] - y
		if y>2 and x<=2:
			x= screen_width-330
			y=screen_height-50
		if y<=2 and x<=2:
			x=screen_width-330
			y=4
		if y<=2 and x>2:
			x=screen_width-100
			y=screen_height-250
	traywnd=win32gui.FindWindow("Shell_TrayWnd","")
	rect=win32gui.GetWindowRect(traywnd)
	if y==4 and rect[2]<int(screen_width/2) and rect[3]>int(screen_height/2):
	 	#print('+')
	 	x=4
	 	y=screen_height-250
	#print(f"Coords:{rect[0]} {rect[1]} Bottom: {rect[2]} {rect[3]}")#" dimensions:{w}x{h}")
	window.geometry(f"120x60+{x}+{y}")


def callback(hwnd, procid):
	global x,y

	if procid in  win32process.GetWindowThreadProcessId(hwnd):
		#win32gui.SetForegroundWindow(hwnd)
		title=win32gui.GetWindowText(hwnd)
		rect=win32gui.GetWindowRect(hwnd)
		if title=='TtkMonitorWindow':

			x = rect[0]
			y = rect[1]
			w = rect[2] - x
			h = rect[3] - y
			win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,x,y,w,h,0)
			x+=int(w/2)
			y+=int(h/2)

def show_window_by_process(procid):
	win32gui.EnumWindows(callback, procid)
	win32gui.EnumWindows(callbackSetWinPosition, None)




img=np.zeros((162,147),np.uint8)
circle_center=img.shape[:2]
cv2.circle(img,circle_center,80,(255,255,255),-1)
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#numpy_horizontal_concat = np.concatenate((img, img), axis=1)
#cv2.imshow('xeyes',img)# numpy_horizontal_concat)
# cv2.circle(img,(66,66),12,(255,0,0),10)
cv2.circle(img,(66,66),12,(255,0,0),10)
show_window_by_process(mypid)
show_frame()
window.mainloop()

# if cv2.waitKey(20) & 0xFF == ord('q'):
# 	break