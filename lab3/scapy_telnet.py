#!/usr/bin/env python
# The first two lines are for not having warnning message
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import argparse
from scapy.all import *

def main():
    ''' 
        Send a telnet SYN using scapy
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="The destination host 198.51.100.1")

    args = parser.parse_args()
    #telnet port: 23
    message = ( (IP(dst=args.host)) / TCP(dport=23,flags='S') )
    message.show()
    answer, unanswer = sr(message)
    answer.show()

if __name__ == "__main__":
    main()
