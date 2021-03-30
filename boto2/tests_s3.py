from boto.s3.key import Key
from helpers import get_bucket,get_S3conn,raise_assertError,get_err_response_status
from decouple import config
from boto.s3.cors import CORSConfiguration
from boto.exception import S3ResponseError
from boto.s3.lifecycle import Lifecycle, Transitions, Rule,Expiration


def test_get_cors():
    """ Check whether GET CORS API call returns 404 since no CORS Rule is set """
    bucket = get_bucket()
    error = raise_assertError(S3ResponseError,bucket.get_cors)
    # assert error.error_code == 'NoSuchCORSConfiguration'
    error_response = get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchCORSConfiguration'

def test_set_cors():
    """
     PUTs arbitraty CORS Rule and checks whether GET CORS API call returns 200 
     and other CORS metadata is as set in PUT call 
    """
    bucket = get_bucket()
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
    bucket = get_bucket()
    assert bucket.delete_cors() == True

def test_get_lifecycle_policy():
    """ Check whether GET lifecycle_policy API call returns 404 since no lifecycle_policy is set """
    bucket = get_bucket()
    error = raise_assertError(S3ResponseError,bucket.get_lifecycle_config)
    # assert error.error_code == 'NoSuchCORSConfiguration'
    error_response = get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchLifecycleConfiguration'

def test_put_lifecycle_policy():
    """
     PUTs arbitraty lifecycle_policy and checks whether GET lifecycle_policy API call returns 200 
     and other lifecycle_policy metadata is as set in PUT call 
    """
    bucket = get_bucket()
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
    bucket = get_bucket()
    assert bucket.delete_lifecycle_configuration() == True

def test_get_bucket_policy():
    """ Check whether GET bucket_policy API call returns 404 since no bucket_policy is set """
    bucket = get_bucket()
    error = raise_assertError(S3ResponseError,bucket.get_lifecycle_config)
    # assert error.error_code == 'NoSuchCORSConfiguration'
    error_response = get_err_response_status(error)
    assert  error_response[0] == 404
    assert  error_response[1] == 'NoSuchLifecycleConfiguration'

# def test_put_bucket_policy():
#     """
#      PUTs arbitraty bucket_policy and checks whether GET bucket_policy API call returns 200 
#      and other bucket_policy metadata is as set in PUT call 
#     """

# def test_delete_bucket_policy():
#     """
#     Deletes bucket_policy and then checks whether GET bucket_policy API call returns 404
#     """


# def test_get_website_configuration():
#     """ Check whether GET website_configuration API call returns 404 since no website_configuration is set """


# def test_put_website_configuration():
#     """
#      PUTs arbitraty website_configuration and checks whether GET website_configuration API call returns 200 
#      and other website_configuration metadata is as set in PUT call 
#     """


# def test_delete_website_configuration():
#     """
#     Deletes website_configuration and then checks whether GET website_configuration API call returns 404
#     """
 

# def test_download_file_missing():
#     """ Tries to download file gsoc-test.txt which isn't yet uploaded,hence gets 404 """


# def test_upload_file():
#     """ Uploads file gsoc-test.txt to bucket and checks whether response StatusCode is 200 """


# def test_delete_file_uploaded():
#     """ Deletes uploaded file gsoc-test.txt and checks whether response StatusCode is 204 """


