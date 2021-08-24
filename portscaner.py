#!/usr/bin/env python

import socket
from termcolor import colored

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.setdefaulttimeout(1)

host=input("[*] Введіть хост для сканування: ")
port=int(input("[*] Введіть порт для сканування: "))
def portscanner(port):
	if sock.connect_ex((host,int(port))):
		print(colored("[!!]Port %d is closed" % (port),'red'))
	else:
		print(colored("[+]Port %d is open" % (port),'blue'))

for port in range(1,100):
    portscanner(port)
