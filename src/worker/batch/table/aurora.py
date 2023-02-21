from . import UploadTable
from sqlalchemy import create_engine
from sqlalchemy.exc import StatementError
import boto3
import pandas as pd
import time

cluster_arn = 'arn:aws:rds:us-east-1:797308887321:cluster:serratus-aurora'
secret_arn = 'arn:aws:secretsmanager:us-east-1:797308887321:secret:rds-db-credentials/cluster-KOFPN4Q2TKDBO5FHY6QO5M3S7Q/serratus-agdBn9'

rdsData = boto3.client('rds-data', region_name='us-east-1')

class AuroraTable(UploadTable):

    def __init__(self, name, cols, keys):
        super().__init__(name, cols)
        self.keys = keys

    def upload_init(self):
        sql = pd.io.sql.get_schema(self.df, self.name)
        execute_sql(sql)
        sql = f"ALTER TABLE {self.name} ADD PRIMARY KEY ({','.join(self.keys)});"
        execute_sql(sql)

    def upload(self):
        if not self.rows:
            return
        engine = create_engine('postgresql+auroradataapi://:@/summary',
            connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn))
        retry_count = 0
        while retry_count < 5:
            try:
                return self.try_upload(engine)
            except StatementError as e:  # botocore.errorfactory.StatementTimeoutException
                if not 'StatementTimeoutException' in str(e):
                    raise e
                retry_count += 1
                time.sleep(2 ** retry_count)
        return self.try_upload(engine)

    def try_upload(self, engine):
        with engine.connect() as con:
            self.df.to_sql(self.name, con,
                if_exists='append',
                index=False)

    def upload_teardown(self):
        sql = f'TRUNCATE {self.name};'
        execute_sql(sql)


def execute_sql(sql):
    rdsData.execute_statement(
        resourceArn=cluster_arn,
        secretArn=secret_arn,
        database='summary',
        sql=sql)
