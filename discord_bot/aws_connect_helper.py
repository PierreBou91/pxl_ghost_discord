import boto3
from os import environ
from io import BytesIO

s3 = boto3.resource(
    service_name='s3',
    aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=environ['AWS_ACCESS_SECRET'])

ghost_bucket = s3.Bucket(environ['AWS_BUCKET_NAME'])

def get_ghost(number):
    return BytesIO(ghost_bucket.Object(f'{number}.png').get()['Body'].read())