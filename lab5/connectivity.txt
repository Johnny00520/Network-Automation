#!/bin/env python3

import netmiko, json, subprocess

def checkConnectivity(devices):
    
    for device in devices:
        pingOutput = subprocess.check_output(['ping', '-c', '4', device['ip']])
        
        print(pingOutput)
        connection = netmiko.ConnectHandler(**device)      
        print(connection.send_command('ping {}'.format(device['ip'])))

def main():
    with open('sshInfo.json') as device_file:
        devices = json.load(device_file)
    checkConnectivity(devices)

if __name__ == '__main__':
    main()
