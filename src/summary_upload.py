import boto3
import io
import json
s3 = boto3.client('s3')

upload_bucket = 'serratus-athena'
upload_dir_run = 'run'
upload_dir_family = 'family'
upload_dir_sequence = 'sequence'

def upload_summary(summary):
    upload_properties(summary)
    upload_families(summary)
    # upload_sequences(summary)

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
    with io.BytesIO() as f:
        f.write(json_str.encode())
        f.seek(0)
        s3.upload_fileobj(f, upload_bucket, object_name)
