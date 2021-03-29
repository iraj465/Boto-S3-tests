from boto.s3.key import Key
from helpers import get_bucket,get_S3conn
from decouple import config

def test_something():
    s3 = get_S3conn()
    r = s3.lookup(config('BUCKET_NAME'))
    assert r == None