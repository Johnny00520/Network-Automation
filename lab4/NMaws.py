#!/bin/env python
import boto3
import time
from datetime import datetime, date, time, timedelta

s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAJCS3LUAIQ4YBIAKQ',
    aws_secret_access_key='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',
    #aws_session_token=SESSION_TOKEN,
)

# Create a bucket
s3_client.create_bucket(
    Bucket="netman-lab5-chch6597",
    CreateBucketConfiguration={
        'LocationConstraint': 'us-west-1'
    }
)

#Upload file
s3 = boto3.resource('s3')
s3.meta.client.upload_file(
    '/home/netman/Documents/netman/midterm/obj3-snmp.txt', #path of file
    'netman-lab5-chch6597',
    'obj3_snmp_timestamp' # desire name of file on S3
)

my_bucket = s3.Bucket('netman-lab5-chch6597')

# print content of bucket
bucketContent = s3_client.list_buckets()
print bucketContent
# List all current buckets
for s3_file in my_bucket.objects.all():
    print(s3_file)

resObj = s3_client.head_object(
    Bucket='netman-lab5-chch6597',
    IfModifiedSince=datetime(2015, 1, 1),
    Key='obj3_snmp_timestamp',
)

print ""

lastModified = resObj.get('LastModified')
expires = resObj.get('LastModified') + timedelta(minutes=30)
expires = expires.isoformat()
print 'LastModified date: ', lastModified
print '30 minutes later expires: ', expires

response = s3_client.put_bucket_lifecycle_configuration(
    Bucket='netman-lab5-chch6597',
    LifecycleConfiguration={
        'Rules': [
            {
                'Expiration': {
                    #'Days': expires,
                    'Days': 1,
                    'ExpiredObjectDeleteMarker': True
                },
                'ID': '1-min-to-glacier',
                'Prefix': "",
                'Status': 'Enabled',
                'Transitions': [
                    {
                        'Days': 0,
                        'StorageClass': 'GLACIER'
                    },
                ],
                'NoncurrentVersionTransitions': [
                    {
                        'NoncurrentDays': 1,
                        'StorageClass': 'GLACIER'
                    },
                ],
                'NoncurrentVersionExpiration': {
                    'NoncurrentDays': 2
                }
            },
        ]
    }
)

