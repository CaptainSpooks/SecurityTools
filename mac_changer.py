#!/usr/bin/env python

import subprocess
import optparse
import re

def  get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="MAC address to change to")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please enter an Interface")
    if not options.new_mac:
        parser.error("[-] Please enter a MAC address")
    return options

def mac_changer(interface, new_mac):
    print("[+] Changing interface " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] Mac_Address changed successfully to: " + new_mac)

def display_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] No MAC Address available, perhaps different interface")


options = get_arguments()
current_mac = display_mac(options.interface)
print("[+] Current MAC Address: " + str(current_mac))
mac_changer(options.interface, options.new_mac)
current_mac = display_mac(options.interface)

if current_mac == options.new_mac:
    print("MAC CHANGED TO" + current_mac)
else:
    print("MAC not changed")



















#Below we have code that does the same thang, however is vulnerable to code escape because of lack of sanitization
# subprocess.call("ifconfig  " + interface + " down",shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac ,shell=True)
# subprocess.call("ifconfig " + interface + " up",shell=True)