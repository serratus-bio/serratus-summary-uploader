from . import UploadTable
from sqlalchemy import create_engine
import boto3
import pandas as pd

cluster_arn = 'arn:aws:rds:us-east-1:797308887321:cluster:serratus-aurora'
secret_arn = 'arn:aws:secretsmanager:us-east-1:797308887321:secret:rds-db-credentials/cluster-KOFPN4Q2TKDBO5FHY6QO5M3S7Q/serratus-agdBn9'

rdsData = boto3.client('rds-data')

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
        if not self.entries:
            return
        engine = create_engine('postgresql+auroradataapi://:@/summary',
            connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn))
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
