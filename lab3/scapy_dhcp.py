#!/usr/bin/env python
# The first two lines are for not having warnning message
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import argparse
from scapy.all import *

def main():
    ''' 
        Send a DHCP Discover message using scapy
    '''
    message = (( Ether(src="32:10:84:f2:3d:27", dst="ff:ff:ff:ff:ff:ff") ) / 
              (IP(src="0.0.0.0", dst="255.255.255.255") ) /  
              (UDP(sport=68, dport=67) ) /
              (BOOTP(chaddr="1248985094c8", xid=RandInt()) ) /
              (DHCP(options=[("message-type", "discover"), "end"]) ))

    message.show()
    sendp(message, iface='tap0')

if __name__ == "__main__":
    main()

