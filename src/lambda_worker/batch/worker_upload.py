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

upload_bucket = 'serratus-athena'
upload_dir_index = 'uploader-index'
upload_dir_run = 'run3'
upload_dir_fam = 'family3'
upload_dir_seq = 'sequence3'

athena_database = 'summarytest'
athena_run_table = 'run'
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

parquet_mode = 'append'

run_cols = ['sra', 'readlength', 'genome', 'version', 'date']
fam_cols = ['run', 'fam', 'famcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname']
seq_cols = ['run', 'seq', 'seqcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name']

def clear():
    wr.catalog.delete_table_if_exists(database=athena_database, table=athena_run_table)
    wr.catalog.delete_table_if_exists(database=athena_database, table=athena_fam_table)
    wr.catalog.delete_table_if_exists(database=athena_database, table=athena_seq_table)
    wr.s3.delete_objects(f's3://{upload_bucket}/{upload_dir_run}')
    wr.s3.delete_objects(f's3://{upload_bucket}/{upload_dir_fam}')
    wr.s3.delete_objects(f's3://{upload_bucket}/{upload_dir_seq}')
    # TODO: clear processed index

def upload_runs(runs):
    wr.s3.to_parquet(
        df=pd.DataFrame(runs)[run_cols],
        path=f"s3://{upload_bucket}/{upload_dir_run}/",
        dataset=True,
        mode=parquet_mode,
        database=athena_database,
        table=athena_run_table
    )

def upload_fams(fams):
    wr.s3.to_parquet(
        df=pd.DataFrame(fams)[fam_cols],
        path=f"s3://{upload_bucket}/{upload_dir_fam}/",
        dataset=True,
        mode=parquet_mode,
        database=athena_database,
        table=athena_fam_table,
        partition_cols=projection_types.keys(),
        projection_enabled=True,
        projection_types=projection_types,
        projection_ranges=projection_ranges
    )

def upload_seqs(seqs):
    wr.s3.to_parquet(
        df=pd.DataFrame(seqs)[seq_cols],
        path=f"s3://{upload_bucket}/{upload_dir_seq}/",
        dataset=True,
        mode=parquet_mode,
        database=athena_database,
        table=athena_seq_table,
        partition_cols=projection_types.keys(),
        projection_enabled=True,
        projection_types=projection_types,
        projection_ranges=projection_ranges
    )

def upload_index(summary_batch):
    # TODO: write processed index
    object_name = f'{upload_dir_index}/{summary_batch.id}.txt'
    upload_string('\n'.join(summary_batch.run_ids), object_name)

def already_uploaded(run_id):
    # TODO: check processed index
    pass

def upload_string(string, object_name):
    with io.BytesIO(string.encode()) as f:
        s3.upload_fileobj(f, upload_bucket, object_name, ExtraArgs={'ACL': 'public-read'})
