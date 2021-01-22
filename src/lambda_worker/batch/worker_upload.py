import boto3
import io
import json
import awswrangler as wr
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

mode = 'append'

upload_bucket = 'serratus-athena'
upload_dir_index = 'uploader-index'
upload_dir_run = 'run3'
upload_dir_fam = 'family3'
upload_dir_seq = 'sequence3'

athena_database = 'summarytest'
athena_fam_table = 'fam'
athena_seq_table = 'seq'

projection_types = {
    'score': "integer",
    'pctid':"integer"
}
projection_ranges = {
    'score': "0,100",
    'pctid':"0,100"
}
seq_partitions = ['score', 'pctid']

def clear():
    wr.catalog.delete_table_if_exists(database=athena_database, table=athena_fam_table)
    wr.s3.delete_objects(f's3://{upload_bucket}/{upload_dir_fam}')

def upload_index(summary_batch):
    object_name = f'{upload_dir_index}/{summary_batch.id}.txt'
    upload_string('\n'.join(summary_batch.run_ids), object_name)

def upload_fams(fams):
    df = pd.DataFrame(fams)
    s3_path = f"s3://{upload_bucket}/{upload_dir_fam}/"
    table = athena_fam_table
    upload_df_as_parquet(df, s3_path, table)

def upload_df_as_parquet(df, s3_path, table):
    wr.s3.to_parquet(
        df=df,
        path=s3_path,
        dataset=True,
        mode=mode,
        partition_cols=projection_types.keys(),
        projection_enabled=True,
        projection_types=projection_types,
        projection_ranges=projection_ranges,
        database=athena_database,
        table=table
    )

def already_uploaded(run_id):
    pass

def upload_string(string, object_name):
    with io.BytesIO(string.encode()) as f:
        s3.upload_fileobj(f, upload_bucket, object_name, ExtraArgs={'ACL': 'public-read'})
