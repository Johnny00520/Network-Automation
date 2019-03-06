#!/bin/env python3
import netmiko
import json, os

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                    netmiko.ssh_exception.NetMikoAuthenticationException)
def main():
    try:
        with open('sshInfo.json') as device_file:
            devices = json.load(device_file)
    
        for device in devices:
            try:
                print('Connecting to', device['ip'])
                connection = netmiko.ConnectHandler(**device)
                print(connection.send_command('show ip interface br'))
                connection.disconnect()

            except netmiko_exceptions as e:
                print("Failed to ", device['ip'], e)
        
    except FileNotFoundError:
        print("File not found")

if __name__ == '__main__':
    main()    
