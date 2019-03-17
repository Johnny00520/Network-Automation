#!/bin/env python3

from flask import Flask, jsonify, request, render_template
from napalm import get_network_driver
import datetime, os, json, socket
from prettytable import PrettyTable

import netmiko
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                    netmiko.ssh_exception.NetMikoAuthenticationException)

def migration():
    try:
        R1srcIP = '198.51.101.1'
        R3destIP = '172.16.1.3'
        R4srcIP = '198.51.101.4'

        keepPinging = True

        R1_driver = get_network_driver('ios')
        R1_ios_router = R1_driver(R1srcIP, 'johnny', 'lab123')
        R1_ios_router.open()
        
        R4_driver = get_network_driver('ios')
        R4_ios_router = R4_driver(R4srcIP, 'johnny', 'lab123')
        R4_ios_router.open()
        
        #shutdown = ['conf t', 'interface Fast 0/0', 'shut']
        checkPkt = ['show int f0/0 summary']

        output = list(R4_ios_router.cli(checkPkt).values())
        output = output[0].split('Interface')
        output.pop(0)
        output = output[0].strip().split() 
        RXPS = output[4]
        pkt = output[-4]
        print(output)
        #print(RXPS)
        #print(pkt)
   
        print("R4 interface 0/0 status- {}: {} packet".format(RXPS, pkt) )
 
        #R4_ios_router.load_merge_candidate(config='int f0/0\n' + 'shut\n' + 'end')

        cmd = ['conf t', 'banner motd #Change made for migration in Lab 6#']

        ping = ['ping 172.16.1.3']
        i = 0
        while(i < 2000):    
            print("\n\nR4 interface 0/0 status- {}: {} packet\n\n".format(RXPS, pkt) )
            print(output)
           
            R1_ping_output = R1_ios_router.ping(R3destIP, timeout=4) 
            #R1_ping_output = R1_ios_router.cli(ping)            
            print(R1_ping_output)
            i += 1

        R1_ios_router.close()
        R4_ios_router.close()

        return "Migration completed successfully"
    except netmiko_exceptions as e:
        return "Failed to connect"    

