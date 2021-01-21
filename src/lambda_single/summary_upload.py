import boto3
import io
import json
from botocore.config import Config
from botocore.exceptions import ClientError
config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)
s3 = boto3.client('s3', config=config)

upload_bucket = 'serratus-athena'
upload_dir_run = 'run2'
upload_dir_family = 'family2'
upload_dir_sequence = 'sequence2'

col_fam = 'fam'
col_seq = 'seq'
col_seq_fam = 'family'
col_score = 'score'
col_pctid = 'pctid'

def upload_summary(summary):
    upload_families(summary)
    upload_sequences(summary)
    upload_properties(summary)

def upload_families(summary):
    for family in summary.families:
        object_name = (f'{upload_dir_family}/' +
            f'{col_fam}={family[col_fam]}/' +
            f'{col_score}={family[col_score]}/' +
            f'{col_pctid}={family[col_pctid]}/' +
            f'{summary.run_id}_{family[col_fam]}.json')
        json_str = json.dumps(family)
        upload_json(json_str, object_name)

def upload_sequences(summary):
    for sequence in summary.sequences:
        object_name = (f'{upload_dir_sequence}/' +
            f'{col_seq_fam}={sequence[col_seq_fam]}/' +
            f'{col_seq}={sequence[col_seq]}/' +
            f'{col_score}={sequence[col_score]}/' +
            f'{col_pctid}={sequence[col_pctid]}/' +
            f'{summary.run_id}_{sequence[col_seq]}.json')
        json_str = json.dumps(sequence)
        upload_json(json_str, object_name)

def upload_properties(summary):
    object_name = f'{upload_dir_run}/{summary.run_id}.json'
    json_str = json.dumps(summary.properties)
    upload_json(json_str, object_name)

def upload_json(json_str, object_name):
    with io.BytesIO(json_str.encode()) as f:
        s3.upload_fileobj(f, upload_bucket, object_name, ExtraArgs={'ACL': 'public-read'})

def already_uploaded(run_id):
    object_name = f'{upload_dir_run}/{run_id}.json'
    try:
        s3.get_object(Bucket=upload_bucket, Key=object_name)
        return True
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            return False
        raise ex
