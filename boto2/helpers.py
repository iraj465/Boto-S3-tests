import boto
from decouple import config

def get_S3conn():
    conn = boto.connect_s3(aws_access_key_id=config('ACCESS_KEY'),
                        aws_secret_access_key=config('SECRET_KEY'),
                        host=config('ENDPOINT'))
    return conn

def get_bucket():
    conn = get_S3conn()
    bucket = conn.get_bucket(config('BUCKET_NAME'))
    return bucket

def get_err_response_status(response):
    status_code = response.args[0]
    error_code = response.error_code
    return tuple([status_code, error_code])

def raise_assertError(exception_class, s3_API_Obj, *args, **kwargs):
    try:
        res = s3_API_Obj(*args, **kwargs)
        print(res)
    except exception_class as e:
        return e