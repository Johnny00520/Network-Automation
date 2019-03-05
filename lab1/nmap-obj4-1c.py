#!/bin/env python
## Reference: https://stackoverflow.com/questions/14026529/python-parse-file-for-ip-addresses
import os, sys 
try:
    import re
except ImportError:
    print "Missing re module"
    sys.exit(1)

# -n: turns off reverse name resolution
# nmap -n -sn 192.0.2.0/24 -oG - | awk '/Up$/{print $2}'
cmd = '/usr/bin/nmap -n -sP 172.20.74.0/24'

process = os.popen(cmd)
results = str(process.read())
ips = []
for result in results.splitlines():
    #Regex for ip address pattern
    ip = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', result) 
    if ip: 
        ips.append(ip)
    else:
        pass
f = open("ips.txt", "w+")
#c = open("ips.csv", "w+")
for ip in ips:
    print ip[0]
    f.write(ip[0] + "\n")
#    c.write(ip[0]+"\n")

