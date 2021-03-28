import boto3
import pytest 
import json
from decouple import config
from boto3.exceptions import S3UploadFailedError 
from botocore.exceptions import ClientError
from utils import get_S3client,raise_assertError,get_response_status,bucket_policy_config,cors_config,lifecycle_config,website_config,get_response_body

def test_download_file_missing():
    """ Tries to download file test.txt which isn't yet uploaded,hence gets 404 """
    client = get_S3client()
    error = raise_assertError(ClientError,client.download_file,Bucket=config('BUCKET_NAME'),Key='test.txt',Filename='test.txt')
    assert  get_response_status(error.response) == 404

def test_upload_file():
    """ Uploads file test.txt to bucket and checks whether response StatusCode is 200 """
    client = get_S3client()
    client.put_object(Bucket=config('BUCKET_NAME'),Key='test.txt',Body=b'foo bar')
    response = client.get_object(Bucket=config('BUCKET_NAME'), Key='test.txt')
    assert get_response_body(response) == 'foo bar'
    assert  get_response_status(response) == 200

def test_delete_file_uploaded():
    """ Deletes uploaded file test.txt and checks whether response StatusCode is 204 """
    client = get_S3client()
    response = client.delete_object(Bucket=config('BUCKET_NAME'), Key='test.txt')
    assert  get_response_status(response) == 204

def test_get_cors():
    """ Check whether GET CORS API call returns 404 since no CORS Rule is set """
    client = get_S3client()
    # GET CORS before setting CORS Rules should raise error
    error = raise_assertError(ClientError,client.get_bucket_cors,Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

def test_put_cors():
    """
     PUTs arbitraty CORS Rule and checks whether GET CORS API call returns 200 
     and other CORS metadata is as set in PUT call 
    """
    client = get_S3client()
    #PUT CORS Rules
    client.put_bucket_cors(Bucket=config('BUCKET_NAME'), CORSConfiguration=cors_config())
    response = client.get_bucket_cors(Bucket=config('BUCKET_NAME'))
    assert response['CORSRules'][0]['AllowedMethods'] == ['GET', 'PUT']
    assert response['CORSRules'][0]['AllowedOrigins'] == ['*.get', '*.put']
    assert get_response_status(response) == 200

def test_delete_cors():
    """
    Deletes CORS Rules and then checks whether GET CORS API call returns 404
    """
    client = get_S3client()
    client.delete_bucket_cors(Bucket=config('BUCKET_NAME'))
    error = raise_assertError(ClientError, client.get_bucket_cors, Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

def test_get_bucket_policy():
    """ Check whether GET bucket_policy API call returns 404 since no bucket_policy is set """
    client = get_S3client()
    error = raise_assertError(ClientError,client.get_bucket_policy,Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

def test_put_bucket_policy():
    """
     PUTs arbitraty bucket_policy and checks whether GET bucket_policy API call returns 200 
     and other bucket_policy metadata is as set in PUT call 
    """
    client = get_S3client()
    client.put_bucket_policy(Bucket=config('BUCKET_NAME'), Policy=bucket_policy_config())
    response = client.get_bucket_policy(Bucket=config('BUCKET_NAME'))
    assert response['Policy'] == bucket_policy_config()
    assert get_response_status(response)== 200

def test_delete_bucket_policy():
    """
    Deletes bucket_policy and then checks whether GET bucket_policy API call returns 404
    """
    client = get_S3client()
    client.delete_bucket_policy(Bucket=config('BUCKET_NAME'))
    error = raise_assertError(ClientError, client.get_bucket_policy, Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

def test_get_lifecycle_policy():
    """ Check whether GET lifecycle_policy API call returns 404 since no lifecycle_policy is set """
    client = get_S3client()
    error = raise_assertError(ClientError,client.get_bucket_lifecycle_configuration,Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

def test_put_lifecycle_policy():
    """
     PUTs arbitraty lifecycle_policy and checks whether GET lifecycle_policy API call returns 200 
     and other lifecycle_policy metadata is as set in PUT call 
    """
    client = get_S3client()
    client.put_bucket_lifecycle_configuration(Bucket=config('BUCKET_NAME'),LifecycleConfiguration=lifecycle_config())
    response = client.get_bucket_lifecycle_configuration(Bucket=config('BUCKET_NAME'))
    assert response['Rules'] == lifecycle_config()['Rules']
    assert get_response_status(response) == 200

def test_delete_lifecycle_policy():
    """
    Deletes lifecycle_policy and then checks whether GET lifecycle_policy API call returns 404
    """
    client = get_S3client()
    client.delete_bucket_lifecycle(Bucket=config('BUCKET_NAME'))
    error = raise_assertError(ClientError, client.get_bucket_lifecycle_configuration, Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

def test_get_website_configuration():
    """ Check whether GET website_configuration API call returns 404 since no website_configuration is set """
    client = get_S3client()
    error = raise_assertError(ClientError,client.get_bucket_website,Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

def test_put_website_configuration():
    """
     PUTs arbitraty website_configuration and checks whether GET website_configuration API call returns 200 
     and other website_configuration metadata is as set in PUT call 
    """
    client = get_S3client()
    client.put_bucket_website(Bucket=config('BUCKET_NAME'),WebsiteConfiguration=website_config())
    response = client.get_bucket_website(Bucket=config('BUCKET_NAME'))
    assert response['IndexDocument'] == website_config()['IndexDocument']
    assert response['ErrorDocument'] == website_config()['ErrorDocument']
    assert get_response_status(response) == 200

def test_delete_website_configuration():
    """
    Deletes website_configuration and then checks whether GET website_configuration API call returns 404
    """
    client = get_S3client()
    client.delete_bucket_website(Bucket=config('BUCKET_NAME'))
    error = raise_assertError(ClientError, client.get_bucket_website, Bucket=config('BUCKET_NAME'))
    assert get_response_status(error.response) == 404

