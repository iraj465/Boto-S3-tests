import boto3
import pytest 
import json
from decouple import config
from boto3.exceptions import S3UploadFailedError 
from botocore.exceptions import ClientError
from utils import get_client,raise_assertError,get_response_status,bucket_policy_config,cors_config

def test_get_cors():
    client = get_client()
    # GET CORS before setting CORS Rules should raise error
    error = raise_assertError(ClientError,client.get_bucket_cors,Bucket=config('BUCKET_NAME'))
    status = get_response_status(error.response)
    assert status == 404


def test_put_cors():
    client = get_client()
    #PUT CORS Rules
    client.put_bucket_cors(Bucket=config('BUCKET_NAME'), CORSConfiguration=cors_config())
    response = client.get_bucket_cors(Bucket=config('BUCKET_NAME'))
    assert response['CORSRules'][0]['AllowedMethods'] == ['GET', 'PUT']
    assert response['CORSRules'][0]['AllowedOrigins'] == ['*.get', '*.put']

def test_delete_cors():
    client = get_client()
    client.delete_bucket_cors(Bucket=config('BUCKET_NAME'))
    error = raise_assertError(ClientError, client.get_bucket_cors, Bucket=config('BUCKET_NAME'))
    status = get_response_status(error.response)
    assert status == 404

def test_get_bucket_policy():
    client = get_client()
    error = raise_assertError(ClientError,client.get_bucket_policy,Bucket=config('BUCKET_NAME'))
    status = get_response_status(error.response)
    assert status == 404

def test_put_bucket_policy():
    client = get_client()
    client.put_bucket_policy(Bucket=config('BUCKET_NAME'), Policy=bucket_policy_config())
    response = client.get_bucket_policy(Bucket=config('BUCKET_NAME'))
    assert response['Policy'] == bucket_policy_config()

def test_delete_bucket_policy():
    client = get_client()
    client.delete_bucket_policy(Bucket=config('BUCKET_NAME'))
    error = raise_assertError(ClientError, client.get_bucket_policy, Bucket=config('BUCKET_NAME'))
    status = get_response_status(error.response)
    assert status == 404

