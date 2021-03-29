import boto3
import pytest 
import json
from decouple import config
from boto3.exceptions import S3UploadFailedError 
from botocore.exceptions import ClientError 

def get_S3client(client_config=None):
    client = boto3.client(service_name='s3',
                        region_name= config('REGION'),
                        aws_access_key_id=config('ACCESS_KEY'),
                        aws_secret_access_key=config('SECRET_KEY'),
                        endpoint_url=config('ENDPOINT_URL'))
    return client

def get_response_body(response):
    body = response['Body']
    bytesBody = body.read()
    if type(bytesBody) is bytes:
        bytesBody = bytesBody.decode()
    return bytesBody

def get_response_status(response):
    status = response['ResponseMetadata']['HTTPStatusCode']
    return status

def raise_assertError(exception_class, s3_API_Obj, *args, **kwargs):
    try:
        s3_API_Obj(*args, **kwargs)
    except exception_class as e:
        return e
    else:
        if hasattr(exception_class, '__name__'):
            exception_name = excClass.__name__
        else:
            exception_name = str(exception_class)
        raise AssertionError("%s not raised" % exception_name)

def cors_config():
    #Sets arbitrary cors metadata for testing purposes
    return {
        'CORSRules': [
            {'AllowedMethods': ['GET', 'PUT'],
             'AllowedOrigins': ['*.get', '*.put'],
            },
        ]
    }
def bucket_policy_config():
    # Sets arbitrary bucket_policy for testing purposes
    return json.dumps(
    {
        "Version": "2012-10-17",
        "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": "*"},
        "Action": "s3:ListBucket",
        "Resource": [
            "{}".format("arn:aws:s3:::" + config('BUCKET_NAME') ),
            "{}".format("arn:aws:s3:::" + config('BUCKET_NAME') + "/*")
          ]
        }]
     })

def lifecycle_config():
    # Sets arbitrary lifecycle_policy for testing purposes
    return {
        'Rules': [
            {'ID': 'rule1', 'Expiration': {'Days': 3}, 'Prefix': 'test1/', 'Status':'Enabled'},
            {'ID': 'rule2', 'Expiration': {'Days': 2}, 'Prefix': 'test2/', 'Status':'Disabled'}
        ]
    }

def website_config():
    # Sets arbitrary website_configuration for testing purposes
    return {
        'IndexDocument': {"Suffix": "index.html"},
        'ErrorDocument': {"Key": "error.html"}
    }