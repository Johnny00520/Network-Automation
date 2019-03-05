#!/bin/env python
import subprocess

class Router:
    '''
        Global attribute 
    '''
    # Sets are unordered.
    # Set elements are unique. Duplicate elements are not allowed.
    # A set itself may be modified, but the elements contained in the set must be of an immutable type.
    oids = {"ifName": ".1.3.6.1.2.1.31.1.1.1.1",
            "ifInUcastPkts": ".1.3.6.1.2.1.2.2.1.11",
            "ifOperStatus": ".1.3.6.1.2.1.2.2.1.8",
            "ifPhysAddress": ".1.3.6.1.2.1.2.2.1.6",
            "ifAdminStatus": ".1.3.6.1.2.1.2.2.1.7",
            "ifIndex": ".1.3.6.1.2.1.2.2.1.1",
            "ifAlias": ".1.3.6.1.2.1.31.1.1.1.18",
            "ifInUcastPkts": ".1.3.6.1.2.1.2.2.1.11",
            "ipAdEntIfIndex": "1.3.6.1.2.1.4.20.1.2",
            "ifDescr": "1.3.6.1.2.1.2.2.1.2",
            "ipAdEntAddr": ".1.3.6.1.2.1.4.20.1.1",
            "ipAdEntNetMask": "1.3.6.1.2.1.4.20.1.3"
            }

    def __init__(self, ipAddr, communityPW):

        self.ipAddr = ipAddr
        self.communityPW = communityPW

        self.ifIndex = self.snmpbulkwalk2(self.oids['ifIndex'])
        self.ifName = self.snmpbulkwalk2(self.oids['ifName'])

        self.ipAdEntIfIndex = self.snmpbulkwalk2(self.oids['ipAdEntIfIndex'])
        self.ifAlias = self.snmpbulkwalk2(self.oids['ifAlias'])

        self.ifOperStatus = self.snmpbulkwalk2(self.oids['ifOperStatus'])
        self.ifPhysAddress = self.snmpbulkwalk2(self.oids['ifPhysAddress'])

        self.ifInUcastPkts = self.snmpbulkwalk2(self.oids['ifInUcastPkts'])
        self.ifAdminStatus = self.snmpbulkwalk2(self.oids['ifAdminStatus'])

        self.Ipv4AdEntAddress = self.snmpbulkwalk2(self.oids['ipAdEntAddr'])
        self.Ipv4AdEntNetMask = self.snmpbulkwalk2(self.oids['ipAdEntNetMask'])

        self.ipAdEntMask = [None] * len(self.ifIndex)
        self.ipAdEntAddress = [None] * len(self.ifIndex)

        #print self.ipAdEntIfIndex
        #print self.ifIndex
        #print self.ipAdEntAddress 
        #print self.ifIndex.index

        for i, j in enumerate(self.ipAdEntIfIndex):
            self.ipAdEntMask[self.ifIndex.index(j)] = self.Ipv4AdEntNetMask
            self.ipAdEntAddress[self.ifIndex.index(j)] = self.Ipv4AdEntAddress

        #print self.Ipv4AdEntAddress
        #print self.Ipv4AdEntNetMask

    def snmpbulkwalk2(self, oid):
        outputs = subprocess.check_output(['snmpbulkwalk', "-v", "2c", "-c", self.communityPW, self.ipAddr, oid]).split('\n')
        result = []
#        print outputs

        for output in outputs:
            output = output.rsplit('=')[-1].strip()
            result.append(output.split(':', 1)[-1].strip())

        if result[-1] == '':
            result.pop()
        return result

    def printOutput(self):
        for i, j in enumerate(self.ifIndex):

            #if self.ifAlias[i] != '':
            #    print "     {}     {}    {}    {}    {}    {}".format(self.ifName[i], self.ifAlias[i], self.ifOperStatus[i], self.ifPhysAddress[i], self.ifAdminStatus[i], self.ifInUcastPkts[i]) 
            if self.ifAlias[i] == '':
                print "     %5s" % self.ifName[i] + "%23s" % self.ifAlias[i] + "%10s" % self.ifOperStatus[i] + "%  20s" % self.ifPhysAddress[i] + " %10s" % self.ifAdminStatus[i] + "  %10s" % self.ifInUcastPkts[i] + "  %25s" % self.Ipv4AdEntAddress +"  %25s" % self.Ipv4AdEntNetMask



R1 = Router('198.51.100.1', 'public')
R2 = Router('198.51.100.2', 'public')
R3 = Router('198.51.100.3', 'public')

print '     Name      Description    OperationalStatus    PhyAddress    AdminStatus    InUniPktCounter      IPv4Addr                IPv4Mask'
print "R1:"
R1.printOutput()
print "R2:"
R2.printOutput()
print "R3:"
R3.printOutput()


