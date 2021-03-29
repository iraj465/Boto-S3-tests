from boto.s3.connection import S3Connection
from decouple import config

def get_S3conn():
    conn = S3Connection(config('ACCESS_KEY'), config('SECRET_KEY'))
    return conn

def get_bucket():
    conn = get_S3conn()
    bucket = conn.get_bucket(config('BUCKET_NAME'))
    return bucket