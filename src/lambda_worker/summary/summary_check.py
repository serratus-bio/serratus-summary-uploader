import boto3
from botocore.exceptions import ClientError
s3 = boto3.client('s3')

upload_bucket = 'serratus-athena'
upload_dir_run = 'run2'

def already_uploaded(run_id):
    object_name = f'{upload_dir_run}/{run_id}.json'
    try:
        s3.get_object(Bucket=upload_bucket, Key=object_name)
        return True
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            return False
        raise ex
