#!/bin/env python
import sys, os, re, json, subprocess
from itertools import izip_longest

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class Router:
    oids = {
            "ifName": ".1.3.6.1.2.1.31.1.1.1.1",
            #IPv4 addr
            "ipAdEntIfIndex": ".1.3.6.1.2.1.4.20.1.1",
            #IPv4 mask
            "ipAdEntNetMask": "1.3.6.1.2.1.4.20.1.3",

            #MAC addr
            "ifPhysAddress": ".1.3.6.1.2.1.2.2.1.6",
            #Interface status
            "ifOperStatus": ".1.3.6.1.2.1.2.2.1.8",
            #IPv6
            "ipv6Address": "1.3.6.1.2.1.4.34.1.5"
            #IPv6 mask
            }

    def __init__(self, ipAddr, communityPW):
        self.ipAddr = ipAddr
        self.communityPW = communityPW
        #self.ifIndex = self.snmpbulkwalk2(self.oids['ifIndex'])
        self.IPv4AdEntIfIndex = self.snmpbulkwalk2(self.oids['ipAdEntIfIndex'])
        self.IPv4AdEntNetMask = self.snmpbulkwalk2(self.oids['ipAdEntNetMask'])

        #interface name
        self.ifName = self.snmpbulkwalk2(self.oids['ifName'])
        # up/down
        self.ifOperStatus = self.snmpbulkwalk2(self.oids['ifOperStatus'])
        #self.ifPhysAddress = self.snmpbulkwalk2(self.oids['ifPhysAddress'])

        #self.ifAdminStatus = self.snmpbulkwalk2(self.oids['ifAdminStatus'])
        #self.ifInUcastPkts = self.snmpbulkwalk2(self.oids['ifInUcastPkts'])
        self.IPv6AdEntAddr = self.snmpbulkwalk2(self.oids['ipv6Address'])

    def snmpbulkwalk2(self, oid):
        outputs = subprocess.check_output(['snmpbulkwalk', "-v", "2c", "-c", self.communityPW, self.ipAddr, oid]).split('\n')
        result = []

        for output in outputs:
            output = output.rsplit('=')[-1].strip()
            result.append(output.split(':', 1)[-1].strip())

        if result[-1] == '':
            result.pop()
        return result

    def convertIPv4Addr(self):
        IPv4Addres = [{ "v4" : { i for i in self.IPv4AdEntIfIndex } }]

        #IPv4Addres = zip(IPv4Addres, self.convertIPv6Addr())

        #IPv4Addres.update(self.convertIPv6Addr())
        print IPv4Addres

        return IPv4Addres

    def convertIPv6Addr(self):
        if(len(self.IPv6AdEntAddr) == 3):
            firstInt = self.IPv6AdEntAddr[1].rsplit('"')
            mask = list(firstInt[-1])
            mask[0] = '/'
            mask = ''.join(mask)
            firstInt = firstInt[-1] + mask

            IPv6_dict = {
                'v6': {firstInt}
            }
            return IPv6_dict

        else:
            firstInt = self.IPv6AdEntAddr[2].rsplit('"')
            mask = list(firstInt[-1])
            mask[0] = '/'
            mask = ''.join(mask)
            firstInt = firstInt[-2] + mask

            secondInt = self.IPv6AdEntAddr[3].rsplit('"')
            mask = list(secondInt[-1])
            mask[0] = '/'
            mask = ''.join(mask)
            secondInt = secondInt[-2] + mask

            IPv6_dict = {
                'v6': {firstInt, secondInt}
            }

            return IPv6_dict

    def JSONdisplayAddr(self):
        for i in range(len(self.IPv4AdEntIfIndex)):
            if(self.IPv4AdEntNetMask[i] == '255.255.255.0'):
                self.IPv4AdEntIfIndex[i] = self.IPv4AdEntIfIndex[i] + '/24'
            else:
                pass

        addr_dict = { k : v for k, v in zip(self.ifName, self.convertIPv4Addr()) }

        addr_dict.update(self.convertIPv6Addr())

        return addr_dict

    def JSONdisplayInterface(self):
        new_interface_dict = { k : v for k, v in zip(self.ifName, self.ifOperStatus)}
        return new_interface_dict

R1 = Router('192.168.0.1', 'public')
R2 = Router('192.168.1.1', 'public')
R3 = Router('192.168.1.2', 'public')
R4 = Router('198.51.100.1', 'public')
R5 = Router('192.168.1.15', 'public')

R1_addr_dict = { "R1": { "addresses": R1.JSONdisplayAddr() }}
R2_addr_dict = { "R2": { "addresses": R2.JSONdisplayAddr() }}
R3_addr_dict = { "R3": { "addresses": R3.JSONdisplayAddr() }}
R4_addr_dict = { "R4": { "addresses": R4.JSONdisplayAddr() }}
R5_addr_dict = { "R5": { "addresses": R5.JSONdisplayAddr() }}

addresListDict = dict(
    R1_addr_dict.items() +
    R2_addr_dict.items() +
    R3_addr_dict.items() +
    R4_addr_dict.items() +
    R5_addr_dict.items()
    )

R1_intFace = { "Router1": { "R2": { "Interface Name": R1.JSONdisplayInterface() }  }}
R2_intFace = { "Router2": { "R2": { "Interface Name": R2.JSONdisplayInterface() }  }}
R3_intFace = { "Router3": { "R3": { "Interface Name": R3.JSONdisplayInterface() }  }}
R4_intFace = { "Router4": { "R4": { "Interface Name": R4.JSONdisplayInterface() }  }}
R5_intFace = { "Router4": { "R5": { "Interface Name": R5.JSONdisplayInterface() }  }}

intListDict = dict(
    R1_intFace.items() +
    R2_intFace.items() +
    R3_intFace.items() +
    R4_intFace.items() +
    R3_intFace.items()
    )

entireList = dict(addresListDict.items() + intListDict.items())
#print entireList
with open('obj3-snmp.txt', 'w') as outfile:
    outfile.write(json.dumps(entireList, cls=SetEncoder, indent=4, separators=(',', ':'), sort_keys=True ))

