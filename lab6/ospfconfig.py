#!/bin/env python3

from flask import Flask, jsonify, request, render_template
from napalm import get_network_driver
import datetime, os, json, socket, sqlite3
from prettytable import PrettyTable

import netmiko
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                    netmiko.ssh_exception.NetMikoAuthenticationException)

def ospf_config(username, password, IPaddr, IPaddr2, pid, pid2, area_id, area_id2, loopbackIP):
    try:

        if not os.path.isfile('lab6.db'):
            print('The database already exist, now connecting to the database...')

            conn = sqlite3.connect('lab6.db')
            c = conn.cursor() #allow us to excuse SQL command

            c.execute('''CREATE TABLE IF NOT EXISTS ospf
                            (name text primary key,
                            username text not null,
                            password text not null,
                            pid int not null,
                            area_id int not null,
                            loopbackIP text not null)''')

        else:
            conn = sqlite3.connect('lab6.db')
            c = conn.cursor() #allow us to excuse SQL command

        if(IPaddr == '198.51.101.2' or IPaddr== '172.16.1.2' or IPaddr == '198.51.101.4' or IPaddr == '172.16.1.2'): 
        
            try:
                socket.inet_aton(IPaddr)
                driver = get_network_driver('ios')            
                ios_router = driver(IPaddr, username, password)
                ios_router.open()

                outputs = ios_router.get_interfaces_ip()
            
                table = PrettyTable(['interfaces', 'IP addresses'])
                for interface, address in outputs.items():
                    table.add_row([interface, address])
                print(table)

                ios_router.load_merge_candidate(config='router ospf ' + pid + '\nnetwork ' + IPaddr + ' 255.255.255.0 area ' + area_id + '\nnetwork ' + IPaddr2 + ' 255.255.255.0 area ' + area_id2 + '\nnetwork ' + loopbackIP + ' 255.255.255.0 area ' + area_id2 + '\nnetwork ' + loopbackIP + ' 255.255.255.0 area ' + area_id + '\nend\nwr\n')
                
                ios_router.commit_config()
                ios_router.close()
 
            except socket.error:
                print("{} is not valid".format(IPaddr))

        else:
            try:
                socket.inet_aton(IPaddr)

                driver = get_network_driver('ios')            
                ios_router = driver(IPaddr, username, password)
                ios_router.open()                

                outputs = ios_router.get_interfaces_ip()
                table = PrettyTable(['interfaces', 'IP addresses'])
                for interface, address in outputs.items():
                    table.add_row([interface, address])
                print(table)

                ios_router.load_merge_candidate(config='router ospf ' + pid + '\nnetwork '+ IPaddr +' 255.255.255.0 area ' + area_id + '\nnetwork ' + loopbackIP + ' 255.255.255.0 area ' + area_id + '\nend\n'+ '\nwr\n')
                ios_router.commit_config()

                if(IPaddr == '198.51.101.1'):
                    name = 'R1'
                    t = (name,)
                    c.execute("SELECT name FROM ospf WHERE name=?", t)
                    #print(type(c.fetchone()))
                    #print(c.fetchall())
                    #print(c.fetchone())
                    if not c.fetchone():
                        c.execute("INSERT INTO ospf VALUES (?,?,?,?,?,?)", (name, username, password, pid, area_id, loopbackIP))
                        print('{} data has been inserted!'.format(name))
                    else:
                        c.execute('UPDATE ospf SET username = ?, password=?, pid=?, area_id=?, loopbackIP=? WHERE name=?', (username, password, pid, area_id, loopbackIP, name))
                        print('{} data has been updated!'.format(name))

                    conn.commit()
                    conn.close()

                    cli = ['ping 20.0.0.1', 'ping 30.0.0.1', 'ping 40.0.0.1']
                
                    resultPing = ios_router.cli(cli)
                    pingTable = PrettyTable(['Action', 'Result'])
                    for action, result in resultPing.items():
                        pingTable.add_row([action, result])
                    return pingTable

                ios_router.close()

            except socket.error as e:
                #print(e)
                print("{} is not valid".format(IPaddr))

    except netmiko_exceptions as e:
        return "Failed to connect: ", IPaddr
