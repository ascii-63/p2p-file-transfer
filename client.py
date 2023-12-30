import os
import sys
import socket
import json
from enum import Enum
from scapy.all import ARP, Ether, srp


ENV_FILE_PATH = '.env'
ARP_TIMEOUT = 1
STORAGE_DIR = 'p2p_storage'


class ExitCode(Enum):
    SUCCESS = 1
    ENV_LOAD_ERR = 2
    ENV_PARSE_ERR = 3
    NET_SCAN_ERR = 4
    OS_LIST_FILES_ERR = 5


class Choice(Enum):
    EXIT = 0
    LIST_NET_PEERS = 1
    LIST_NET_FILES = 2
    LIST_LOCAL_FILES = 3
    DOWNLOAD = 4


host = ''
port = 10000
network_address = ''


######################################################################

def networkScan(_network_address):
    """
    Return list of hosts in a Network Address
    """

    # Create an ARP request packet to get local IP addresses
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=_network_address)
    # Send the packet and receive the response
    result = srp(arp_request, timeout=ARP_TIMEOUT, verbose=0)[0]
    # Extract the IP addresses
    hosts = [response[1].psrc for response in result]

    return hosts


def getFilesInDir(_dir_path):
    """
    Get all files in a directory
    """

    files = [f for f in os.listdir(_dir_path) if os.path.isfile(
        os.path.join(_dir_path, f))]
    return files


def envParser():
    """
    Parse the .env file to get config about:
    1. This client IP Address
    2. The Network Address
    """

    global host
    global network_address

    try:
        with open(ENV_FILE_PATH) as file:
            for line in file:
                if line.strip() and not line.strip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"Error when read .env file: {e} \n")
        return ExitCode.ENV_LOAD_ERR

    try:
        host = os.environ.get('IP_ADDRESS')
        network_address = os.environ.get('NETWORK_ADDRESS')
    except Exception as e:
        print(f"Error while parse .env file: {e}")
        return ExitCode.ENV_PARSE_ERR

    return ExitCode.SUCCESS


def displayMenu():
    """
    Display the choice menu after clear the terminal screen
    """
    os.system('clear')

    print(f"*****************************************")
    print(f"*        P2P File Share Client          *")
    print(f"*  Credit: https://github.com/acsii-63  *")
    print(f"*****************************************")
    print(f"\nClient IP Address: {host}")
    print(f"\nMenu:")
    print(f"0. Exit the client.")
    print(f"1. List all peers in the network.")
    print(f"2. List all files in the network.")
    print(f"3. List all files in my storage.")
    print(f"4. Download a file.")
    print(f"\n*****************************************")


######################################################################


def menu_listPeers():
    print(f"*******************************************************")
    print(f"*                                                     *")
    print(f"*  LIST ALL THE ACTIVE PEERS IN THE P2P FILE NETWORK  *")
    print(f"*                                                     *")
    print(f"*******************************************************")
    print(f"\nNetwork Address: {network_address}\n")

    try:
        peers = networkScan(network_address)
    except Exception as e:
        print(f"Error when scan for host in the network: {e}")
        return ExitCode.NET_SCAN_ERR

    index = 1
    for peer in peers:
        print(f"Peer {index}: {peer}")
        index += 1

    return ExitCode.SUCCESS


def menu_listNetFiles():
    return ExitCode.SUCCESS


def menu_listLocalFiles():
    print(f"*******************************************")
    print(f"*                                         *")
    print(f"*  LIST ALL FILES IN THIS CLIENT STORAGE  *")
    print(f"*                                         *")
    print(f"*******************************************")

    this_dir = os.getcwd()
    storage_dir = this_dir + '/' + STORAGE_DIR
    print(f"\nStorage directory: {storage_dir}\n")

    try:
        files = getFilesInDir(storage_dir)
    except Exception as e:
        print(f"Error when scan for files in this client storage: {e}")
        return ExitCode.OS_LIST_FILES_ERR

    index = 1
    for file in files:
        print(f"{index}. {file}")
        index += 1

    print(f"\nFile count: {len(files)}")

    return ExitCode.SUCCESS


def menu_downloadFile():
    return ExitCode.SUCCESS


def choiceHandle(_choice):
    """
    Handle user choice to call the feature function
    """

    os.system('clear')

    choice = int(_choice)

    if choice == Choice.EXIT.value:
        print(f"Exiting the Client...")
        sys.exit(0)

    elif choice == Choice.LIST_NET_PEERS.value:
        result = menu_listPeers()
        if result != ExitCode.SUCCESS:
            print(
                f"Failed to get the list of peers in the network. (Exit code: {result}) \n")
        return ExitCode.SUCCESS

    elif choice == Choice.LIST_NET_FILES.value:
        result = menu_listNetFiles()
        if result != ExitCode.SUCCESS:
            print(
                f"Failed to get the list of files in the network. (Exit code: {result}) \n")
        return ExitCode.SUCCESS

    elif choice == Choice.LIST_LOCAL_FILES.value:
        result = menu_listLocalFiles()
        if result != ExitCode.SUCCESS:
            print(
                f"Failed to get the list of files in this client. (Exit code: {result}) \n")
        return ExitCode.SUCCESS

    elif choice == Choice.DOWNLOAD.value:
        result = menu_downloadFile()
        if result != ExitCode.SUCCESS:
            print(
                f"Failed to download file. (Exit code: {result}) \n")
        return ExitCode.SUCCESS

    print(f"Invalid choice.")


def afterChoiceHandle():
    """
    This function handle after a feature is completed.
    Ask the user want to exit or back to menu
    """

    while True:
        print(f"\n*****************************************\n")
        print(f"0. Exit the client.")
        print(f"1. Back to client menu")

        choice_str = input("\nEnter your next move: ")
        choice = int(choice_str)

        if (choice == 0):
            print(f"Exiting the Client...")
            sys.exit(0)
        elif (choice == 1):
            return None

        print(f"Invalid input!")
        os.system('clear')


######################################################################


if __name__ == "__main__":
    env_par_res = envParser()
    if (env_par_res != ExitCode.SUCCESS):
        sys.exit(env_par_res)

    while True:
        displayMenu()

        choice_str = input("\nEnter your choice: ")
        choiceHandle(choice_str)
        afterChoiceHandle()
