from __future__ import print_function
from botocore.vendored import requests
from collections import defaultdict, Counter
import boto3
import base64, time, json, sys



s3 = boto3.client('s3')
kinesis = boto3.client('kinesis')



def lambda_handler(event, context):
    s3_data = defaultdict(lambda: defaultdict(set))

    records = []
  
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        # We also assume payload comes as JSON form
        payload = json.loads(base64.b64decode(record['kinesis']['data']))
        
        log_events = payload.get('logEvents', [])
        for log_event in log_events:
            message = log_events['message'].split()
            srcaddr = message[3]
            dstaddr = message[4]
            action = message[12]
            
            if action == 'REJECT':
                reject_count = Counter(action)
                s3_data[reject_count][srcaddr].add[dstaddr]
                s3_data[reject_count][dstaddr].add[srcaddr]
                print ('reject_count')
            else:
                print ("No REJECT connections")
                
    for reject_count in sorted(s3_data):
        output_data = {k: len(v) for k, v in s3_data[reject_count]}
        obj = s3.Object('dwolla-technical-exercise', 'problem1')
        s3.put_object(Body=json.dumps(output_data))
        