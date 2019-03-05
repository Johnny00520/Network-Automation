#!/bin/env python
# Reference: https://docs.python.org/2/library/datetime.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics
import sys 
import time
try:
    import boto3
    import smtplib
    from datetime import timedelta
    from datetime import datetime
    from pprint import pprint
except ImportError:
    print 'Missing module/s'
    sys.exit(1) 

def checkInstances(ec2):
    runningInstancesList = []
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        runningInstancesList.append(instance.id)
    return sorted(runningInstancesList)

def getMetricStat(client, metricName, metricUnit, stat, instanceId):
    result = client.get_metric_statistics(
        #time interval needs to be at least 30 minutes
        StartTime = datetime.utcnow() - timedelta(minutes=30),
        EndTime = datetime.utcnow() + timedelta(minutes=5),
        MetricName = metricName,
        Period = 3600,
        Namespace = 'AWS/EC2',
        Statistics=[stat],
        Unit = metricUnit,
        Dimensions=[{'Name':'InstanceId', 'Value': instanceId}]
        )
    return str(result['Datapoints'][0][stat])

def shutdownInstance(ec2, instanceId):
    ec2.instances.filter(InstanceIds=[instanceId]).stop()

ec2 = boto3.resource('ec2')
client = boto3.client('cloudwatch')
runningInstancesID = checkInstances(ec2)
toAddr = "chch6597@colorado.edu"
fromAddr = "chch6597@colorado.edu"
email_username = "chch6597@colorado.edu"
userPwd = 'johnny_77520'
threshold = 0.9

server = smtplib.SMTP()
server.connect('smtp.gmail.com')
server.ehlo()
server.starttls()
server.login(email_username, userPwd)
header = 'To:' + toAddr + '\n' + 'From: ' + email_username + '\n' + 'Subject: Instance shutting down \n'
while(True):
    for instanceId in runningInstancesID:
        CPUStat = float(getMetricStat(client, 'CPUUtilization', 'Percent', 'Maximum', instanceId))
        print CPUStat
        if CPUStat > threshold:
            print instanceId + ' is not fine. Threshold is {} '.format(threshold)
            print "Shuting down..."
            shutdownInstance(ec2, instanceId)
            message = " \n" + header + "\n\n " + instanceId + " is above threshold." + "\n\n" + "This instance is shutting down"
            server.sendmail(toAddr, fromAddr, message)
            server.quit()
            time.sleep(90)
        else:
            print instanceId + ' is still fine. Threshold is: {} '.format(threshold)


