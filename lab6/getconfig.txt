#!/bin/env python3

from flask import Flask, jsonify, request, render_template
#app = Flask(__name__)
from napalm import get_network_driver
import datetime, os, json

ipsList = [
    '198.51.100.1', #R1
    '198.51.101.2', #R2
    '172.16.1.3',   #R3
    '198.51.101.4'  #R4
]

def getconfig():
    arr = []   
 
    for i in range(len(ipsList)):
        print("Connecting to: ", ipsList[i])
        driver = get_network_driver('ios')
        ios_router = driver(ipsList[i], 'johnny', 'lab123')
        ios_router.open()

        output = ios_router.get_config()
        output = str(output).replace("\'", "\"") 

        now = datetime.datetime.now().isoformat()

        with open('R' + str(i + 1) + '_' + now + '.txt', 'a') as outfile:
            json.dump(output, outfile)
        outfile.close()

        ios_router.close()
        arr.append(os.path.basename(outfile.name))

    strings = ', '.join(arr)
    return "You have saved the files: " + strings
