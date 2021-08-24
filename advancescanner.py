#!/usr/bin/env python
from socket import *
import optparse
from threading import *

def get_arguments():
    parser=optparse.OptionParser('Usage of program: ' + '-H <target host> -p <target port>')
    parser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
    parser.add_option('-p',dest='tgtPort',type='string',help='specify target ports separated by comma')
    (options,args) = parser.parse_args()
    return options

def connScan(tgtHost,tgtPort):
    try:
        sock=socket(AF_INET,SOCK_STREAM)
        sock.connect((tgtHost,tgtPort))
        print('[+]%d/tcp Open' % tgtPort)
    except:
        print('[-] %d/tcp Closed' % tgtPort)
    finally:
        sock.close()

def portScan(tgtHost,tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print('Unknown host %s' %tgtHost)
    try:
        tgtName= gethostbyaddr(tgtIP)
        print('[+] Scan Results for: '+tgtName[0])
    except:
        print('[+] Scan Results for: '+tgtIP)
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t=Thread(target=connScan,args=(tgtHost,int(tgtPort)))
        t.start()

def main():
    # parser=optparse.OptionParser('Usage of program: ' + '-H <target host> -p <target port>')
    # parser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
    # parser.add_option('-p',dest='tgtPort',type='string',help='specify target ports separated by comma')
    # (options,args) = parser.parse_args()
    usage='Usage of program: ' + '-H <target host> -p <target port>'
    options=get_arguments()
    tgtHost=options.tgtHost
    tgtPorts=str(options.tgtPort).split(',')
    if (tgtHost == None) | (tgtPorts[0]==None):
        #print(parser.usage)
        print(usage)
        exit(0)
    portScan(tgtHost,tgtPorts)

if __name__== '__main__':
    main()