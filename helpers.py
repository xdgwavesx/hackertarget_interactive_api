import os
import socket


def clear_screen():
    os.system('cls||clear')


def network_is_online():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        print('[!] Checking Network Status.....')
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
