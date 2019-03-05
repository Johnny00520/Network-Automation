#!/bin/env python
import boto3

def showInstances(ec2):
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    for instance in instances:
        print(instance.id, instance.instance_type, instance.public_ip_address, instance.state['Name'])

def launchInstances(ec2, myAMI_ubuntu, instanceType):
    ec2.create_instances(ImageId=myAMI_ubuntu, MinCount=1, MaxCount=2)

def getLaunchTime(ec2):
    ec2List = []
    instances = ec2.instances.filter()
    for instance in instances:
        ec2List.append((instance.launch_time, instance.id))
    return sorted(ec2List)[0]

def stopInstance(ec2, newbieId):
    print(newbieId)
    ec2.instances.filter(InstanceIds=[newbieId]).stop()

# public amazon ubuntu AMI
myAMI_ubuntu = 'ami-0799ad445b5727125'
instanceType = 't2.micro'
ec2 = boto3.resource('ec2')

instances = ec2.instances.filter()

instancesNum = 0
for i in instances:
    instancesNum += 1
    print instancesNum

if instancesNum < 4:
    launchInstances(ec2, myAMI_ubuntu, instanceType)
    newbie, newbieId = getLaunchTime(ec2)
    print newbie
    print newbieId
    stopInstance(ec2, newbieId)

#newbie, newbieId = getLaunchTime(ec2) 
showInstances(ec2)
