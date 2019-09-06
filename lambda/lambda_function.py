from __future__ import print_function
import requests
import json
import urllib
import boto3

s3 = boto3.client('s3')

url= "http://<domain/ip for api backend>:5000/api"

def lambda_handler(event, context):
    if event['Records'][0]['eventName'] in ['ObjectRemoved:DeleteMarkerCreated']:
        r = requests.get(url + '/rename/' + '?objectkey=' + event['Records'][0]['s3']['object']['key'] + '&bucketname=' + event['Records'][0]['s3']['bucket']['name'])
        record = r.json()
        if type(record) == str:
            return None
        if  event['Records'][0]['s3']['object']['key'] in record['objectkey']:
            event['Records'][0]['s3']['object']['eTag'] = record['etag']
            event['Records'][0]['s3']['object']['size'] = None

            data = payload_data(event)

            r = requests.post(url, json=data)
            return (r.status_code, r.reason)
        return None
        
        
    if event['Records'][0]['eventName'] in [ 'ObjectRemoved:Delete']:

        r = requests.get(url + '/' + '?objectkey=' + event['Records'][0]['s3']['object']['key'] + '&bucketname=' + event['Records'][0]['s3']['bucket']['name'] + '&versionId=' + event['Records'][0]['s3']['object']['versionId'])

        record = r.json()
        if type(record) == str:
            return None
        if  event['Records'][0]['s3']['object']['key'] in record['objectkey']:
            event['Records'][0]['s3']['object']['eTag'] = record['etag']
            event['Records'][0]['s3']['object']['size'] = None

            data = payload_data(event)
            r = requests.put(url + '/' + '?objectkey=' + event['Records'][0]['s3']['object']['key'] + '&bucketname=' + event['Records'][0]['s3']['bucket']['name'] + '&versionId=' + event['Records'][0]['s3']['object']['versionId'] , json=data)
            return (r.status_code, r.reason)
        return None
    
        
    if event['Records'][0]['eventName'] in [ 'ObjectCreated:Put', 'ObjectCreated:CompleteMultipartUpload', 'ObjectCreated:Copy']:
        data = payload_data(event)
        r = requests.post(url, json=data)
        return (r.status_code, r.reason)


def payload_data(event):
    
    try:
        size = round(event['Records'][0]['s3']['object']['size'] /1048576, 2)
    except:
        size = event['Records'][0]['s3']['object']['size']
        
        
    data = { "eventVersion": event['Records'][0]['eventVersion'] , 
    "eventSource": event['Records'][0]['eventSource'], "awsRegion": event['Records'][0]['awsRegion'], 
    "eventTime": event['Records'][0]['eventTime'], "eventName": event['Records'][0]['eventName'], 
    "principalId": event['Records'][0]['userIdentity']['principalId'], 
    "sourceIPAddress": event['Records'][0]['requestParameters']['sourceIPAddress'],
    "s3SchemaVersion":event['Records'][0]['s3']['s3SchemaVersion'] , 
    "configurationId": event['Records'][0]['s3']['configurationId'] ,
    "bucketname": event['Records'][0]['s3']['bucket']['name'],
    "bucketarn": event['Records'][0]['s3']['bucket']['arn'] ,"objectkey": event['Records'][0]['s3']['object']['key'],
    "objectsize": size, "etag": event['Records'][0]['s3']['object']['eTag'], 
    "versionId": event['Records'][0]['s3']['object']['versionId'], "sequencer":event['Records'][0]['s3']['object']['sequencer']}
    return data
