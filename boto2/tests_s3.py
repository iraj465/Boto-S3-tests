from boto.s3.key import Key
import helpers
from decouple import config
from boto.s3.cors import CORSConfiguration
from boto.exception import S3ResponseError
from boto.s3.lifecycle import Lifecycle, Transitions, Rule,Expiration


def test_get_cors():
    """ Check whether GET CORS API call returns 404 since no CORS Rule is set """
    bucket = helpers.get_bucket()
    error = helpers.raise_assertError(S3ResponseError,bucket.get_cors)
    # assert error.error_code == 'NoSuchCORSConfiguration'
    error_response = helpers.get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchCORSConfiguration'

def test_set_cors():
    """
     PUTs arbitraty CORS Rule and checks whether GET CORS API call returns 200 
     and other CORS metadata is as set in PUT call 
    """
    bucket = helpers.get_bucket()
    cors_cfg = CORSConfiguration()
    # Setting arbitrary CORS Rule which allows cross-origin GET requests from all origins.
    cors_cfg.add_rule('POST', 'https://www.example.com', allowed_header='*', max_age_seconds=3000, expose_header='x-amz-server-side-encryption')
    bucket.set_cors(cors_cfg)
    response = bucket.get_cors()
    assert 'https://www.example.com' in response[0].allowed_origin

def test_delete_cors():
    """
    Deletes CORS Rules and then checks whether GET CORS API call returns 404
    """
    bucket = helpers.get_bucket()
    assert bucket.delete_cors() == True

def test_get_lifecycle_policy():
    """ Check whether GET lifecycle_policy API call returns 404 since no lifecycle_policy is set """
    bucket = helpers.get_bucket()
    error = helpers.raise_assertError(S3ResponseError,bucket.get_lifecycle_config)
    # assert error.error_code == 'NoSuchCORSConfiguration'
    error_response = helpers.get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchLifecycleConfiguration'

def test_set_lifecycle_policy():
    """
     PUTs arbitraty lifecycle_policy and checks whether GET lifecycle_policy API call returns 200 
     and other lifecycle_policy metadata is as set in PUT call 
    """
    bucket = helpers.get_bucket()
    transitions = Transitions()
    transitions.add_transition(days=30, storage_class='STANDARD_IA')
    transitions.add_transition(days=90, storage_class='GLACIER')
    expiration = Expiration(days=120)
    rule = Rule(id='ruleid', prefix='logs/', status='Enabled', expiration=expiration, transition=transitions)
    lifecycle = Lifecycle()
    lifecycle.append(rule)
    assert bucket.configure_lifecycle(lifecycle) == True

def test_delete_lifecycle_policy():
    """
    Deletes lifecycle_policy and then checks whether GET lifecycle_policy API call returns 404
    """
    bucket = helpers.get_bucket()
    assert bucket.delete_lifecycle_configuration() == True

def test_get_bucket_policy():
    """ Check whether GET bucket_policy API call returns 404 since no bucket_policy is set """
    bucket = helpers.get_bucket()
    error = helpers.raise_assertError(S3ResponseError,bucket.get_policy)
    error_response = helpers.get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchBucketPolicy'

def test_set_bucket_policy():
    """
     PUTs arbitraty bucket_policy and checks whether GET bucket_policy API call returns 200 
     and other bucket_policy metadata is as set in PUT call 
    """
    bucket = helpers.get_bucket()
    assert bucket.set_policy(helpers.bucket_policy_config(bucket.name)) == True

def test_delete_bucket_policy():
    """
    Deletes bucket_policy and then checks whether GET bucket_policy API call returns 404
    """
    bucket = helpers.get_bucket()
    assert bucket.delete_policy() == True


def test_get_website_configuration():
    """ Check whether GET website_configuration API call returns 404 since no website_configuration is set """
    bucket = helpers.get_bucket()
    error = helpers.raise_assertError(S3ResponseError,bucket.get_website_configuration)
    error_response = helpers.get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchWebsiteConfiguration'
    

def test_set_website_configuration():
    """
     PUTs arbitraty website_configuration and checks whether GET website_configuration API call returns 200 
     and other website_configuration metadata is as set in PUT call 
    """
    bucket = helpers.get_bucket()
    assert bucket.set_website_configuration_xml(helpers.bucket_website_config()) == True
    


def test_delete_website_configuration():
    """
    Deletes website_configuration and then checks whether GET website_configuration API call returns 404
    """
    bucket = helpers.get_bucket()
    assert bucket.delete_website_configuration() == True
 

def test_get_file_missing_from_key():
    """ Tries to download file gsoc-test.txt which isn't yet uploaded,hence gets 404 """
    bucket = helpers.get_bucket()
    k = Key(bucket=bucket)
    k.key = 'gsoc-test.txt'
    error = helpers.raise_assertError(S3ResponseError,k.get_contents_as_string)
    error_response = helpers.get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchKey'

def test_get_file_from_key():
    """ Simple Upload file-string gsoc-test.txt to bucket and checks whether response StatusCode is 200 """
    bucket = helpers.get_bucket()
    k = Key(bucket=bucket)
    k.key = 'gsoc-test.txt'
    k.set_contents_from_string('foobar')
    assert k.get_contents_as_string() == bytes('foobar','utf-8')

def test_delete_file_uploaded():
    """ Deletes uploaded file gsoc-test.txt and checks whether response StatusCode is 204 """
    bucket = helpers.get_bucket()
    k = Key(bucket=bucket)
    k.key = 'gsoc-test.txt'
    k.delete()
    error = helpers.raise_assertError(S3ResponseError,k.get_contents_as_string)
    error_response = helpers.get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchKey'

