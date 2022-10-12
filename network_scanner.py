#!/usr/bin/env python
# this project uses p2

import scapy.all as scapy  # Arp lib
import argparse  # Allows to create arguments

argument_list = [ 
    {
     "short_code": "-t",
     "code": "--target",
     "dest": "raw_target",
     "help_text": "Target who will be tested"
    }
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

# Setting default behavior if the arguments are not defined
target = raw_target if raw_target else "192.168.67.1/24"

# Checking if there's arguments and if not, define default values
not raw_target and print("[+] Target argument is not set, using " + target + " as default.")


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n---------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


scan_result = scan(target)
print_result(scan_result)


# arp_request_broadcast.show()
# arp_request.pdst=ip
# scapy.ls(scapy.ARP())



