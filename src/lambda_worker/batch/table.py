import boto3
import pandas as pd

upload_bucket = 'serratus-athena'
athena_database = 'summary'
parquet_mode = 'append'

cluster_arn = ''
secret_arn = ''

rdsData = boto3.client('rds-data')

class UploadTable(object):

    def __init__(self, name, s3_name, s3_dir, cols, projection_enabled=False, projection_types=None, projection_ranges=None):
        self.name = name
        self.cols = cols
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

    def create_table_sql(self):
        sql = pd.io.sql.get_schema(self.df, self.name)
        execute_sql(sql)

    def insert_sql(self, con):
        if not self.entries:
            return
        self.df.to_sql(self.name, con,
            if_exists='append',
            index=False)

    def delete_existing(self):
        sql = f'TRUNCATE {self.name};'
        execute_sql(sql)

def execute_sql(sql):
    rdsData.execute_statement(
        resourceArn=cluster_arn,
        secretArn=secret_arn,
        database='summary',
        sql=sql)
