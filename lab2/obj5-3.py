#!/bin/env python
# Reference: https://docs.python.org/2/library/datetime.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics
import sys
try:
    import boto3
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

ec2 = boto3.resource('ec2')
client = boto3.client('cloudwatch')
runningInstancesID = checkInstances(ec2)

for instanceId in runningInstancesID:
    print "Instance ID: {}".format(instanceId)
    print "Status Check: " + getMetricStat(client, "StatusCheckFailed", "Count", "Maximum", instanceId)
    print "CPU Utilization: " + getMetricStat(client, "CPUUtilization", "Percent", "Average", instanceId)
    print "Network In: " + getMetricStat(client, "NetworkIn", "Bytes", "Average", instanceId)
    print "Network Out: " + getMetricStat(client, "NetworkOut", "Bytes", "Average", instanceId)
    print "\n"


