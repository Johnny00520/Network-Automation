#!/bin/env python3
from ncclient import manager
import json, time, io
import xml.etree.ElementTree as ET

CREATE_INTERFACE_IP = """
    <config>
        <cli-config-data>
            <cmd>hostname Router%s</cmd>
            <cmd>interface %s</cmd>
            <cmd>ip address %s %s</cmd>
            <cmd>no shutdown</cmd>
            <cmd>wr</cmd>
        </cli-config-data>
    </config>
"""

CREATE_OSPF = """
    <config>
        <cli-config-data>
            <cmd>router ospf %s</cmd>
            <cmd>router-id %s</cmd>
            <cmd>network %s %s area %s </cmd>
            <cmd></cmd>
        </cli-config-data>
    </config>
"""


def create_loopback(conn, hostname, interface, ipv4Addr, ipv4mask):
    try:
        config_str = CREATE_INTERFACE_IP % (hostname, interface, ipv4Addr, ipv4mask)
        rpc_sent = conn.edit_config(target='running', config=config_str)
        # c = conn.get_config(source='running', filter=GET_CONFIG)
        # c = conn.get_config(source='running')
        # print(c)
        # print(rpc_sent)

    except Exception:
        print('Exception occurs while creating interface %s' % interface) 

def create_ospf(conn, processId, rid, advAddr, wildMask, OSPF_areaNum):
    try:
        config_str = CREATE_OSPF % (processId, rid, advAddr, wildMask, OSPF_areaNum)
        rpc_sent = conn.edit_config(target='running', config=config_str)
        # print(rpc_sent)

    except Exception:
        print('Exception occurs while creating ospf %s' % processId)

def get_config(conn, j):
    config = conn.get_config('running')

    output = ['R'+str(j)]

    config = str(config)

    config = config.split('\n')
    hostname = config[7].split(' ')

    output.append(hostname[1])

    interface = config[53].split(' ')

    output.append(interface[3])
    output.append('/24')

    ospfconfig = config[125].split(' ')
    output.append(ospfconfig[-1])
    output.append(ospfconfig[2])
    output.append('/24')
    newoutput = []
    for i in output:
        i = i.replace('\r', '')
        newoutput.append(i)

    print(' '.join(newoutput))
    
    # test = ''
    # for i in output:
    #     print(i)
    #     test = test + i
    #     print(test)

    # with open('test.txt', 'a+') as f:
    #     f.write(output)

    # print(output)
    # print(''.join(output))



def conn_config(devices):
    i = 0
    print("Router Hostname Loopback 99 IP OSPF Area  OSPF Network to advertise")
    for device in devices:
        i += 1
        try:
            with manager.connect(
                host = device['host'], 
                port = 22, 
                username = device['username'], 
                password = device['password'],
                hostkey_verify=False, 
                allow_agent=False, 
                look_for_keys=False,
                device_params={'name':'csr'}
                ) as conn_manager:

                create_loopback(
                    conn_manager, 
                    device["R"+str(i)]["identikey"], 
                    device["R"+str(i)]["loopback"], 
                    device["R"+str(i)]["loopbackIP"], 
                    device["R"+str(i)]["loopbackMask"])

                create_ospf(
                    conn_manager,
                    device["R"+str(i)]["ospf"]['processId'],
                    device["R"+str(i)]["ospf"]['routerId'], 
                    device["R"+str(i)]["ospf"]['advIP'], 
                    device["R"+str(i)]["ospf"]['wildMask'], 
                    device["R"+str(i)]["ospf"]['areaNum'])

                get_config(conn_manager, i)

        except:
            pass

def main():
    filename = 'lab9_obj2_requirement.json'
    with open(filename, 'r') as f:
        devices = json.load(f)
        conn_config(devices)

if __name__ == "__main__":
    main()