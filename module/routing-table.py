import os
import sys
import socket
import subprocess
import ipaddress
import re
from scapy.all import ARP, Ether, srp

SIZE = 255
NET_ADD_TAIL = '0/24'


def getLocalIPAdress():
    """
    Return local IP address of this host
    """

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to any remote server (doesn't actually send any data)
        s.connect(("8.8.8.8", 80))
        # Get the local IP address from the connected socket
        local_ip = s.getsockname()[0]
        s.close()

        return local_ip

    except Exception as e:
        print(f"Error: {e}")

        return None


def networkScan(_network_address):
    """
    Return list of hosts in a Network Address
    """

    # Create an ARP request packet to get local IP addresses
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=_network_address)
    # Send the packet and receive the response
    result = srp(arp_request, timeout=1, verbose=0)[0]
    # Extract the IP addresses
    hosts = [response[1].psrc for response in result]

    return hosts


def IPToNetwork(_ip):
    """
    From a IP Address, return it's Network Address
    """

    last_dot_index = _ip.rfind('.')
    substr = _ip[:last_dot_index + 1]
    network_address = substr + NET_ADD_TAIL

    return network_address


if __name__ == "__main__":
    local_ip = getLocalIPAdress()
    net_add = IPToNetwork(local_ip)
    hosts = networkScan(net_add)

    for host in hosts:
        print(host)
