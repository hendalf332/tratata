#!/usr/bin/env python3.9
from subprocess import run,check_output,STDOUT
import optparse
import os
import re

def get_arguments():
    parser=optparse.OptionParser('Usage of program: ' + '--interface <interface> --mac <NEW MAC address>')
    parser.add_option('-i','--interface',dest='interface',type='string',help='interface to change mac address!')
    parser.add_option('-m','--mac',dest='new_mac',type='string',help='NEW MAC address')
    (options,args) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    return options

def change_mac(interface,new_mac):
    print("[+] Changing MAC address for "+interface+" to " +new_mac)
#    run(["ifconfig",interface,"down"])
    st=run(["ifconfig",interface,"down"])
    st=run(["ifconfig",interface,"hw","ether",new_mac])
    st=run(["ifconfig",interface,"up"])

def get_current_mac(interface):
 cmd='/usr/sbin/ifconfig '+interface
 #ifconfig_result=run(cmd).stdout
 ifconfig_result=check_output(["ifconfig",interface])

# print(str(ifconfig_result)+' IFCONFIG RESULT')

 mac_address_search_result=re.search(r'(\w{2}\:){5}\w{2}',str(ifconfig_result))
 if mac_address_search_result:
#  print(mac_address_search_result.group(0))
  return mac_address_search_result.group(0)
 else:
  print("[-] Could not read MAC address.")
os.system("clear")
options=get_arguments()
#print(f'\t your interface {options.interface} newmac {options.new_mac}')
current_mac=get_current_mac(options.interface) 
print("Current MAC="+str(current_mac))
change_mac(options.interface,options.new_mac)
current_mac=get_current_mac(options.interface) 
if current_mac==options.new_mac:
    print("[+] MAC address was successfully changed to "+current_mac)
else:
    print("[-] MAC address did not get changed.")