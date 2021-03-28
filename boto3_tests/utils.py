import boto3
import pytest 
import json
from decouple import config
from boto3.exceptions import S3UploadFailedError 
from botocore.exceptions import ClientError 

def get_client(client_config=None):
    client = boto3.client(service_name='s3',
                        region_name= config('REGION'),
                        aws_access_key_id=config('ACCESS_KEY'),
                        aws_secret_access_key=config('SECRET_KEY'),
                        endpoint_url=config('ENDPOINT_URL'))
    # response = client.list_buckets()
    return client

def _get_status_and_error_code(response):
    status = response['ResponseMetadata']['HTTPStatusCode']
    error_code = response['Error']['Code']
    return status, error_code
def get_response_status(response):
    status = response['ResponseMetadata']['HTTPStatusCode']
    return status

def raise_assertError(excClass, callableObj, *args, **kwargs):
    """
    Like unittest.TestCase.assertRaises, but returns the exception.
    """
    try:
        callableObj(*args, **kwargs)
    except excClass as e:
        return e
    else:
        if hasattr(excClass, '__name__'):
            excName = excClass.__name__
        else:
            excName = str(excClass)
        raise AssertionError("%s not raised" % excName)

def cors_config():
    return {
        'CORSRules': [
            {'AllowedMethods': ['GET', 'PUT'],
             'AllowedOrigins': ['*.get', '*.put'],
            },
        ]
    }
def bucket_policy_config():
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
    return {
        'Rules': [
            {'ID': 'rule1', 'Expiration': {'Days': 1}, 'Prefix': 'test1/', 'Status':'Enabled'},
            {'ID': 'rule2', 'Expiration': {'Days': 2}, 'Prefix': 'test2/', 'Status':'Disabled'}
        ]
    }