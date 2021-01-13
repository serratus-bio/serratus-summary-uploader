import boto3
import io
import json
from botocore.exceptions import ClientError
s3 = boto3.client('s3')

upload_bucket = 'serratus-athena'
upload_dir_run = 'run'
upload_dir_family = 'family'
upload_dir_sequence = 'sequence'

def upload_summary(summary):
    upload_families(summary)
    # upload_sequences(summary)
    upload_properties(summary)

def upload_families(summary):
    for family in summary.families:
        object_name = f'{upload_dir_family}/{summary.run_id}_{family["fam"]}.json'
        json_str = json.dumps(family)
        upload_json(json_str, object_name)

def upload_sequences(summary):
    for sequence in summary.sequences:
        object_name = f'{upload_dir_sequence}/{summary.run_id}_{sequence["seq"]}.json'
        json_str = json.dumps(sequence)
        upload_json(json_str, object_name)

def upload_properties(summary):
    object_name = f'{upload_dir_run}/{summary.run_id}.json'
    json_str = json.dumps(summary.properties)
    upload_json(json_str, object_name)

def upload_json(json_str, object_name):
    with io.BytesIO(json_str.encode()) as f:
        s3.upload_fileobj(f, upload_bucket, object_name)

def already_uploaded(run_id):
    object_name = f'{upload_dir_run}/{run_id}.json'
    try:
        s3.get_object(Bucket=upload_bucket, Key=object_name)
        return True
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            return False
    raise Exception('unknown response')
