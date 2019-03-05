#!/usr/bin/env python
# The first two lines are for not having warnning message
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import argparse
from scapy.all import *

# You need to use sudo in order to run the program
# Like 'sudo python scapy_icmp.py 198.51.100.x'

def main():
    '''
        Build a simple ICMP request using scapy
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="The host to ping IE 198.51.100.1")
    args = parser.parse_args()

    #ICMP
    packets = sr1(IP(dst=args.host)/ICMP())
    packets.show()

if __name__ == "__main__":
    main()


