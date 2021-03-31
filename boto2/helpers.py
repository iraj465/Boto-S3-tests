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
        s3_API_Obj(*args, **kwargs)
    except exception_class as e:
        return e

def bucket_policy_config(bucket_name):
    return '''{
      "Version":"2012-10-17",
      "Statement": [{
        "Sid": "Allow Public Access to All Objects",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Condition": {
                    "StringLikeIfExists": {
                        "aws:Referer": "http://www.example.com/*"
                    }
                },
        "Resource": "arn:aws:s3:::%s/*"
      }
     ]
    }''' % bucket_name

def bucket_website_config():
    fragment = '<ErrorDocument><Key>error.html</Key></ErrorDocument><IndexDocument><Suffix>index.html</Suffix></IndexDocument>'
    return '<?xml version="1.0" encoding="UTF-8"?><WebsiteConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">' + fragment + '</WebsiteConfiguration>'