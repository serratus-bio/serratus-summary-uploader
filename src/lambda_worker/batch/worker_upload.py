import boto3
import io
import json
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
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
upload_dir_index = 'uploader-index'
upload_dir_run = 'run3'
upload_dir_family = 'family3'
upload_dir_sequence = 'sequence3'

fam_partitions = ['fam', 'score', 'pctid']
seq_partitions = ['fam', 'seq', 'score', 'pctid']

def upload_index(summary_batch):
    object_name = f'{upload_dir_index}/{summary_batch.id}.txt'
    upload_string('\n'.join(summary_batch.run_ids), object_name)

def already_uploaded(run_id):
    pass

def upload_fams(fams):
    # partition
    # upload each partition

    df = pd.DataFrame(fams)
    object_name = f'{upload_dir_family}/test.parquet'
    upload_df_as_parquet(df, object_name)

    # for fams in fams:
    #     object_name = (f'{upload_dir_family}/' +
    #         f'{col_fam}={family[col_fam]}/' +
    #         f'{col_score}={family[col_score]}/' +
    #         f'{col_pctid}={family[col_pctid]}/' +
    #         f'{summary.run_id}_{family[col_fam]}.json')
    #     json_str = json.dumps(family)
    #     upload_string(json_str, object_name)


def upload_df_as_parquet(df, object_name):
    table = pa.Table.from_pandas(df)
    # print(table)
    with io.BytesIO() as stream:
        pq.write_table(table, stream, compression='snappy')
        stream.seek(0)
        s3.upload_fileobj(stream, upload_bucket, object_name, ExtraArgs={'ACL': 'public-read'})


def upload_string(string, object_name):
    with io.BytesIO(string.encode()) as f:
        s3.upload_fileobj(f, upload_bucket, object_name, ExtraArgs={'ACL': 'public-read'})
