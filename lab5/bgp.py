#!/bin/env python3
import netmiko, json, sys

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                    netmiko.ssh_exception.NetMikoAuthenticationException)

def CMD_checking(CMD):
    #if(CMD[0].strip().lower() == 'conf'):
    if('c' and 'o' and 'n' and 'f' and ' ' and 't' not in CMD[0].strip().lower()):
        print("Invalid command: Do you mean conf terminal? ")
        return False
    if('r' and 'o' and 'u' and 't' and 'e' and 'r' and ' ' and 'b' and 'g' and 'p' not in CMD[1].strip().lower()):
        print("you should have `router bgp #` command")
        return False
    
    CMD[1].strip()
    if('100' not in CMD[1]):
        print("You should have AS number followed by `router bgp` command")
        return False
    if('n' and 'e' and 'i' and 'g' and 'h' and 'b' and 'o' and 'r' not in CMD[2].strip().lower()):
        print("You should have `neighbor` command, followed by neightbor ip address")
        return False
    if('r' and 'e' and 'm' and 'o' and 't' and 'e' and '-' and 'a' and 's' not in CMD[2].strip().lower()):
        print("You should have `remote-as` command, followed by AS #")
        return False
    if('n' and 'e' and 't' and 'w' and 'o' and 'r' and 'k' and 'm' and 'a' and 's' and 'k' not in CMD[3] and CMD[4]):
        print("You have should `network` and 'mask' commands")
        return False
    return True

def CMD_send(connection, device):
    if('R1_Cheng' in device):
        cmd_lists_R1 = [
            'conf t', 'router bgp ' + device['R1_Cheng']['bgp']['LocalAS'] ,
            'neighbor ' + device['R1_Cheng']['neighbor']['ip'] + ' remote-as ' + device['R1_Cheng']['neighbor']['RemoteAS'] ]

        for prefix in device['R1_Cheng']['bgp']['AdvPrefixes']:
            networkCMD = 'network ' + prefix + ' mask 255.255.255.255'
            cmd_lists_R1.append(networkCMD)
        
        valid = CMD_checking(cmd_lists_R1)
        if(valid):
            connection.send_config_set(cmd_lists_R1)
            for prefix in device['R1_Cheng']['bgp']['AdvPrefixes']:
                networkCMD = 'network ' + prefix + ' mask 255.255.255.255'
                connection.send_config_set(networkCMD)
        else:
            print("Some commands are invalid")
              
    elif('R2_Cheng' in device):
        cmd_lists_R2 = [
            'conf t', 'router bgp ' + device['R2_Cheng']['bgp']['LocalAS'] ,
            'neighbor ' + device['R2_Cheng']['neighbor']['ip'] + ' remote-as ' + device['R2_Cheng']['neighbor']['RemoteAS'] ]

        for prefix in device['R2_Cheng']['bgp']['AdvPrefixes']:
            networkCMD = 'network ' + prefix + ' mask 255.255.255.255'
            cmd_lists_R2.append(networkCMD)
        
        valid = CMD_checking(cmd_lists_R2)

        if(valid): 
            connection.send_config_set(cmd_lists_R2)
        else:
            print("Some commands are invalid")

def displayOutput(output):
    arr = []
    output = output.strip().splitlines()

    for lines in output:
        #arr.append(lines)
        words = lines.split()
        if('neighbor' in lines):
            arr.append(words[3])
        if('remote AS' in lines):
            arr.append(words[6])
        if('BGP' and 'state' in lines):
            arr.append(words[3])
    arr.pop()
    print("{:20s}{:20s}{:20s}".format('BGP Neighbot IP', 'BGP Neighbor AS', 'BGP Neighbor State'))
    print('{:20s}{:20s}{:20s}'.format(arr[0][:-1], arr[1][:-1], arr[2][:-1]))

def displayShowRun(outputShowRun):
    filename = 'showRunOnRouter.txt'
    print("File name is " + filename)
    
    with open(filename, 'a') as f:
        f.write(outputShowRun)
        f.close()

def connectDevices(devices):
    
    for device in devices:
        try:
            print('Connecting to', device['ip'])
            connection = netmiko.ConnectHandler(
                device_type=device['device_type'],
                host=device['ip'],
                username=device['username'],
                password=device['password']
            )
            CMD_send(connection, device)
            output = connection.send_command('show ip bgp neighbors')
            displayOutput(output)
            
            outputShowRun = connection.send_command('show run')
            displayShowRun(outputShowRun)
            connection.disconnect()

        except netmiko_exceptions as e:
            print("Failed to connect ", device['ip'], e)

def main():
    with open('bgp.json') as device_file:
        devices = json.load(device_file)
        #print(devices)
    connectDevices(devices)

if __name__ == '__main__':
    main()
