#!/bin/env python3

import netmiko, json
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                    netmiko.ssh_exception.NetMikoAuthenticationException)

def configOSPF(connect, device):
    OSPF_cmd_list = ['conf t', 'router ospf ' + device['OSPF']['ProcessID'] ]

    for prefix in device['OSPF']['AdvPrefixes']:
        OSPF_cmd_list.append('network ' + prefix + ' 0.0.0.255 area ' + device['OSPF']['AreaNum'])
    OSPF_cmd_list.append('wr')
        
    connect.send_config_set(OSPF_cmd_list)
    print(OSPF_cmd_list) 

def configInts(connect, device):
   # loopbackCmdList = fastetherCmdList = GigaEthernetList = ['conf t']
    RouterintCmdList = ['conf t']

    for interface in device['interfaces']:
#        print(interface)
#        print(interface['loopback'])

        if('loopback' in interface):
            for intface in interface['loopback']:
                #loopbackCmdList.append('int loopback ' + intface['num'])
                #loopbackCmdList.append('ip addr ' + intface['ip'] +' '+ intface['mask'])

                RouterintCmdList.append('int loopback ' + intface['num'])
                RouterintCmdList.append('ip addr ' + intface['ip'] +' '+ intface['mask'])

        if('FastEthernet' in interface):
            for intface in interface['FastEthernet']:
                #fastetherCmdList.append('int f'+ intface['num'])
                #fastetherCmdList.append('ip addr '+ intface['ip'] +' '+ intface['mask'])
                #fastetherCmdList.append('no shut')

                RouterintCmdList.append('int f'+ intface['num'])
                RouterintCmdList.append('ip addr '+ intface['ip'] +' '+ intface['mask'])
                RouterintCmdList.append('no shut')
                RouterintCmdList.append('wr')

        connect.send_config_set(RouterintCmdList)


def read_config(boxes):
    for k, v in boxes.items():
        nested_devices = [v]
        for device in nested_devices:
            try:
                print("Connecting to: " + device['ip'])
                connect = netmiko.ConnectHandler(
                    device_type = device['device_type'],
                    host = device['ip'],
                    username = device['username'],
                    password = device['password'])

                configInts(connect, device)
                configOSPF(connect, device)

                connect.disconnect()

            except netmiko_exceptions as e:
                print("Failed to connect to ", data['ip'])

def main():
    try:
        #with open('requirement.json', 'r') as f:
        with open('test.json', 'r') as f:
            boxes = json.load(f)
            read_config(boxes)

    except FileNotFoundError:
        print("File not found")

if __name__ == "__main__":
    main()
