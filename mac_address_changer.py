#!/usr/bin/env python

import subprocess  # Run SO code
import argparse  # Allows to create arguments
import re  # Allows to use Regex


argument_list = [
    {
     "short_code": "-i",
     "code": "--interface",
     "dest": "raw_interface",
     "help_text": "Interface to change its MAC address"
    },
    {
     "short_code": "-m",
     "code": "--mac",
     "dest": "raw_macAddress",
     "help_text": "New Mac Address"
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


def get_current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)


# Getting options and arguments from parser
options = get_arguments(argument_list)

# Setting into variables the options acquired from the function above
raw_interface = options.raw_interface
raw_macAddress = options.raw_macAddress

# Setting default behavior if the arguments are not defined
mainCommand = "ifconfig"
interface = raw_interface if raw_interface else "eth0"
mac_address = raw_macAddress if raw_macAddress else "00:11:22:33:44:55"

# Command strings who will be concat with the rest of the code
commands = [
    "down",
    "hw ether " + mac_address,
    "up"
]


# Checking if there's arguments and if not, define default values
not raw_interface and print("[+] Interface argument is not set, using " + interface + " as default.")
not raw_macAddress and print("[+] MacAddress argument is not set, using " + mac_address + " as default.")


# Main function that return the progress to de user and make the subprocess.call generically
def subprocess_call(functions):
    print("[+] Changing MAC address for the interface: " + interface)
    current_mac_address = get_current_mac_address(interface)
    current_mac_address and print("[+] Your current MacAddress is: " + current_mac_address)
    print("[+] Running commands...")
    for function in functions:
        formatted_function = mainCommand + " " + interface + " " + function
        print("[>] " + formatted_function)
        subprocess.call(formatted_function, shell=True)
    current_mac_address = get_current_mac_address(interface)
    if current_mac_address == mac_address:
        print("[+] MAC address of " + interface + " Changed successfully to " + mac_address)


subprocess_call(commands)

# ctrl / to comment
# optparse is a module that allows to get arguments from the user

