#!/bin/env python
import sys, subprocess, os
from scapy.all import *
from StringIO import StringIO
#pcapFile = rdpcap("pingC2C3.pcap")
pcapFile = rdpcap("another.pcap")

#R21
capture = StringIO()
save_stdout = sys.stdout
sys.stdout = capture
#R21icmp = pcapFile[21].show()
R21icmp = pcapFile[9].show()
sys.stdout = save_stdout
R21 = capture.getvalue()

R21_addrs = []
for i in R21.splitlines():
    R21_MAC_addr = re.findall(r'(?:[0-9a-fA-F]:?){12}', i)
    if R21_MAC_addr:
        R21_addrs.append(R21_MAC_addr)
    else:
        pass

#R31
capture = StringIO()
save_stdout = sys.stdout
sys.stdout = capture
R31icmp = pcapFile[12].show()
sys.stdout = save_stdout
R31 = capture.getvalue()

R31_addrs = []
for i in R31.splitlines():
    R31_MAC_addr = re.findall(r'(?:[0-9a-fA-F]:?){12}', i)
    if R31_MAC_addr:
        R31_addrs.append(R31_MAC_addr)
    else:
        pass

#print "R21 addresses: ", R21_addrs
for i in R21_addrs:
    print i
print "R21 MAC address: {}".format(R21_addrs[0][0])

print "\n"

#print "R31 addresses: ", R31_addrs
for i in R31_addrs:
    print i
print "R31 MAC address: {}".format(R31_addrs[0][0])
