from boto.s3.connection import S3Connection
from decouple import config

def get_S3conn():
    conn = S3Connection(config('ACCESS_KEY'), config('SECRET_KEY'))
    return conn

def get_bucket():
    conn = get_S3conn()
    bucket = conn.get_bucket(config('BUCKET_NAME'))
    return bucket

def get_response_status(response):
    status = response['ResponseMetadata']['HTTPStatusCode']
    return status

def raise_assertError(exception_class, s3_API_Obj, *args, **kwargs):
    try:
        s3_API_Obj(*args, **kwargs)
    except exception_class as e:
        return e