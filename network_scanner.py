#!/usr/bin/env python
#pip3 install scapy-python3
import scapy.all as scapy
import argparse
import os
import time

def get_arguments():
    parser=argparse.ArgumentParser('Usage of program: ' + '-r <ipaddress>')
    parser.add_argument('-r',dest='ipAddr',help='IP адресса/Діапазон IP адресів')
    options = parser.parse_args()
    if not options.ipAddr:
        parser.error("[-] Please specify an ip address, use --help for more info")
    return options

def scan(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list=scapy.srp(arp_request_broadcast,timeout=3,verbose=False)[0]
    client_list=[]
    for element in answered_list:
        client_dict={"ip":element[1].psrc,"mac":element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result_list):
    print("IP\t\t\tMAC Address")
    print("-"*80)
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])
        
os.system("clear")
options=get_arguments()

try:
    while True:
        scan_result=scan(options.ipAddr)
        os.system("clear")
        print_result(scan_result)
        time.sleep(7)
except KeyboardInterrupt:
    pass
