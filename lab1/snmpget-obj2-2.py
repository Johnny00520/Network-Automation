#!/bin/evn python
import sys, os, re
cmds = [ 
    ['snmpget -v 1 -c public 198.51.100.1 1.3.6.1.2.1.1.4.0',
    'snmpget -v 1 -c public 198.51.100.1 1.3.6.1.2.1.1.5.0',
    'snmpget -v 1 -c public 198.51.100.1 1.3.6.1.2.1.1.6.0',
    'snmpget -v 1 -c public 198.51.100.1 1.3.6.1.2.1.2.1.0',
    'snmpget -v 1 -c public 198.51.100.1 1.3.6.1.2.1.1.3.0'],
    ['snmpget -v 2c -c public 198.51.100.2 1.3.6.1.2.1.1.4.0',
    'snmpget -v 2c -c public 198.51.100.2 1.3.6.1.2.1.1.5.0',
    'snmpget -v 2c -c public 198.51.100.2 1.3.6.1.2.1.1.6.0',
    'snmpget -v 2c -c public 198.51.100.2 1.3.6.1.2.1.2.1.0',
    'snmpget -v 2c -c public 198.51.100.2 1.3.6.1.2.1.1.3.0'],
    ['snmpget -v 3 -l authPriv -u JOHNNY -a SHA -A Netman123 -X Netman123 198.51.100.3 1.3.6.1.2.1.1.4.0',
    'snmpget -v 3 -l authPriv -u JOHNNY -a SHA -A Netman123 -X Netman123 198.51.100.3 1.3.6.1.2.1.1.5.0',
    'snmpget -v 3 -l authPriv -u JOHNNY -a SHA -A Netman123 -X Netman123 198.51.100.3 1.3.6.1.2.1.1.6.0',
    'snmpget -v 3 -l authPriv -u JOHNNY -a SHA -A Netman123 -X Netman123 198.51.100.3 1.3.6.1.2.1.2.1.0',
    'snmpget -v 3 -l authPriv -u JOHNNY -a SHA -A Netman123 -X Netman123 198.51.100.3 1.3.6.1.2.1.1.3.0']
]

outputs = []
titleList = ['Contact:', 'Name:', 'Location:', 'Number:', 'Uptime:']

for i in cmds:
    for j in i:
        #print j
        f = os.popen(j)
        outputs.append(f.read())
#print 'Length of outputs: ', len(outputs)

def splitPrint(subString):
    for i, j in zip(titleList, subString):
        print i, j + "\n"

def print_V1(v1_outputs):
    subString = []
    print "SNMPv1"
    for i in v1_outputs:
        #print "Original output: "+ i
        #test = i.split(":")[1]

        index = i.find('STRING:')
        if index != -1:
            subs = i[index:]
            subs = subs.split(":")[1]
            subString.append(subs)
            #print "Contact: " + subs
            #print subs
        else:
            index = i.find('INTEGER:')
            if index != -1:
                subs = i[index:]
                subs = subs.split(":")[1]
                subString.append(subs)
                #print subs
            else:
                index = i.find("Timeticks:")
                subs = i[index:]
        #        print subs
                subs = re.findall(r'([\d]{1,3}:[\d]{1,3}:[\d]{1,3}.[\d]{1,3})', subs)
                subString.append(subs[0])

    splitPrint(subString)

def print_V2(v2_outputs):
    subString = []
    print "SNMPv2"
    for i in v2_outputs:
        #print "Original output: "+ i
        #test = i.split(":")[1]

        index = i.find('STRING:')
        if index != -1:
            subs = i[index:]
            subs = subs.split(":")[1]
            subString.append(subs)
            #print subs
        else:
            index = i.find('INTEGER:')
            if index != -1:
                subs = i[index:]
                subs = subs.split(":")[1]
                subString.append(subs)
                #print subs
            else:
                index = i.find("Timeticks:")
                subs = i[index:]
        #        print subs
                subs = re.findall(r'([\d]{1,3}:[\d]{1,3}:[\d]{1,3}.[\d]{1,3})', subs)
                subString.append(subs[0])

    splitPrint(subString)

def print_V3(v3_outputs):
    subString = []
    print "SNMPv3"
    for i in v3_outputs:
        #print "Original output: "+ i
        #test = i.split(":")[1]

        index = i.find('STRING:')
        if index != -1:
            subs = i[index:]
            subs = subs.split(":")[1]

            subString.append(subs)
            #print subs
        else:
            index = i.find('INTEGER:')
            if index != -1:
                subs = i[index:]
                subs = subs.split(":")[1]
                subString.append(subs)
                #print subs
            else:
                index = i.find("Timeticks:")
                subs = i[index:]
        #        print subs
                subs = re.findall(r'([\d]{1,3}:[\d]{1,3}:[\d]{1,3}.[\d]{1,3})', subs)
                subString.append(subs[0])

    splitPrint(subString)


counter = 0
v1_outputs = []
v2_outputs = []
v3_outputs = []
for counter in range(len(outputs)):
#    print counter 
    if counter <= 4:
        #print outputs[counter]
        v1_outputs.append(outputs[counter])
    if counter >= 5 and counter <= 9:
        v2_outputs.append(outputs[counter])
    if counter > 9 and counter <= len(outputs):
        v3_outputs.append(outputs[counter])

print_V1(v1_outputs)
print_V2(v2_outputs)
print_V3(v3_outputs)
