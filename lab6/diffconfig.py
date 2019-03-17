#!/bin/env python3

from flask import Flask, jsonify, request, render_template
from napalm import get_network_driver
import datetime, os, json, socket
from prettytable import PrettyTable
import difflib

import netmiko
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                    netmiko.ssh_exception.NetMikoAuthenticationException)

def diffconfig():
    IPlist = [
            #'198.51.101.1', 
            #'198.51.101.2', 
            '172.16.1.3', 
            '198.51.101.4'
            ]
    
    for i in range(len(IPlist)):
        print("\n\nConnecting to: ", IPlist[i] + '\n')
        try:
            driver = get_network_driver('ios')
            ios_router = driver(IPlist[i], 'johnny', 'lab123')
            ios_router.open()
            print(ios_router.compare_config())
            print("\n\n")

            now = datetime.datetime.now().isoformat()
            output = ios_router.get_config()
            output = str(output).replace("\'", "\"") 
 
            with open('new_R' + str(i + 1) + '_' + now + '.txt', 'w') as file1:
                json.dump(output, file1)
            file1.close()

            ios_router.close()

            currectFiles = [f for f in os.listdir( os.curdir ) if os.path.isfile(f)]

            for j in currectFiles:
                if(j.startswith('new_R'+ str(i + 1))):
                    #return j
                    with open(j) as file1:
                        f1_text = file1.readlines()
 
            for j in currectFiles:
                if(j.startswith('R'+ str(i + 1)) and j.endswith('.txt')):
                    with open(j) as file2:
                        f2_text = file2.readlines()

            for line in difflib.unified_diff(f1_text, f2_text):
                print(line + "\n")

        except netmiko_exceptions as e:
            return "Failed to connect: ", ip 

    return 'Compared difference successful. Please go check the terminal!'
