import boto3
import awswrangler as wr
import pandas as pd
import numpy as np

upload_bucket = 'serratus-athena'
athena_database = 'summary'
parquet_mode = 'append'

dynamodb = boto3.resource("dynamodb")

N_KEYS = {'score', 'pctid', 'aln', 'glb', 'len', 'topscore', 'toplen'}
N_KEYS |= {'readlength', 'totalalns'} # protein summary comment
N_KEYS |= {'alns', 'avgcols'} # protein summary lines
N_KEYS |= {'depth'} # double

class UploadTable(object):

    def __init__(self, name, s3_name, s3_dir, cols, partition_key, projection_enabled=False, projection_types=None, projection_ranges=None):
        self.name = name
        self.cols = cols
        self.partition_key = partition_key
        self.entries = []
        self.projection_enabled = projection_enabled
        self.projection_types = projection_types
        self.projection_ranges = projection_ranges
        self.projection_kwargs = {}
        if (projection_enabled):
            self.projection_kwargs = {
                'projection_enabled': True,
                'projection_types': self.projection_types,
                'projection_ranges': self.projection_ranges,
                'partition_cols': self.projection_types.keys()
            }
        self.s3_path = f"s3://{upload_bucket}/{s3_dir}/{s3_name}/"

    def create_dataframe(self):
        if not self.entries:
            return
        self.df = pd.DataFrame(self.entries)[self.cols]

    def upload_s3_glue_parquet(self):
        if not self.entries:
            return
        wr.s3.to_parquet(
            df=self.df,
            path=self.s3_path,
            dataset=True,
            mode=parquet_mode,
            database=athena_database,
            table=self.name,
            **self.projection_kwargs
        )

    def upload_dynamodb(self):
        if not self.entries:
            return
        wr.dynamodb.put_df(
            df=self.df,
            table_name=self.name
        )

    def delete_existing(self):
        wr.catalog.delete_table_if_exists(database=athena_database, table=self.name)
        wr.s3.delete_objects(self.s3_path)

    def create_dynamodb_table(self):
        dynamodb.create_table(
            TableName=self.name,
            KeySchema=[{"AttributeName": self.partition_key, "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": self.partition_key, "AttributeType": 'S'}],
            BillingMode="PAY_PER_REQUEST"
        )

# def dynamodb_create_table(name, df):
#     attribute_definitions = get_dynamodb_attribute_definitions(df)
#     dynamodb.create_table(
#         TableName=name,
#         KeySchema=[{"AttributeName": "sra", "KeyType": "HASH"}],
#         AttributeDefinitions=list(attribute_definitions),
#     )

# dtype_dynamo_map = {
#     np.dtype('O'): 'S',
#     np.dtype('int64'): 'N'
# }

# def get_dynamodb_attribute_definitions(df):
#     for col_name, col_type in zip(df.columns, df.dtypes):
#         yield {
#                 "AttributeName": col_name,
#                 "AttributeType": dtype_dynamo_map[col_type]
#             }