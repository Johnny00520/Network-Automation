#!/bin/env python3
import netmiko, json, socket


def checkValidIPaddr(devices):
    for device in devices:
        try:
            socket.inet_aton(device['ip'])
        
        except socket.error:
            print("{} is not valid".format(device['ip'])) 
        else:
            print("{} is valid".format(device['ip']))

def main():
    with open('sshInfo.json') as device_file:
        devices = json.load(device_file)

    checkValidIPaddr(devices) 

if __name__ == '__main__':
    main()
