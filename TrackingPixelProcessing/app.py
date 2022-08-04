## Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
## SPDX-License-Identifier: MIT-0

from dataclasses import replace
import json
import boto3
import base64
import os
import sys

import traceback

def trace_except(sysexecinfo, smessage = ''):
   """ Trace exceptions """
   exc_type, exc_value, exc_traceback = sysexecinfo
   i, j = (traceback.extract_tb(exc_traceback, 1))[0][0:2]
   k = (traceback.format_exception_only(exc_type, exc_value))[0]
  #  trace('E:'+ 'Err : ' + smessage + k + i + ', ligne ' + str(j))
   return k

kinesis_client = boto3.client('firehose', region_name='us-west-1')
kinesis_firehose = ''

if 'KINESIS_FIREHOSE_STREAM_NAME' in os.environ and os.environ['KINESIS_FIREHOSE_STREAM_NAME'].strip():
    kinesis_firehose = os.environ['KINESIS_FIREHOSE_STREAM_NAME'].strip()
else:
  print("KINESIS_FIREHOSE_STREAM_NAME not found")

def lambda_handler(event, context):
  response = {
  "statusCode": 200,
  "statusDescription": "200 OK",
  "isBase64Encoded": True,
  "headers": {
    "Content-Type": "image/gif" #"text/html" #
    }
   }
  # print("lambda_handler => hello")
  try:
    kresponse = kinesis_client.put_record(DeliveryStreamName=kinesis_firehose,Record={'Data': json.dumps(event, indent=4, sort_keys=True)})
    # response['body'] = json.dumps(kresponse, indent=4, sort_keys=True)
    response['body'] = "R0lGODlhAQABAJAAAP8AAAAAACH5BAUQAAAALAAAAAABAAEAAAICBAEAOw==" #'<b>ok hihi</b>' #json.dumps(event, indent=4, sort_keys=True) #

  except: #Catch all exceptions, we don't want the analytical part affects the business process so they are only printed in the logs
    response['body'] = 'kinesis_firehose=' + kinesis_firehose + '<br/>error: ' + trace_except(sys.exc_info())
    response['isBase64Encoded'] = False
    response['headers']['Content-Type'] = 'text/html'
  
  return response
