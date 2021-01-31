from . import UploadTable
from sqlalchemy import create_engine
import boto3
import pandas as pd

cluster_arn = ''
secret_arn = ''

rdsData = boto3.client('rds-data')

class AuroraTable(UploadTable):

    def __init__(self, name, cols):
        super().__init__(name, cols)

    def upload_init(self):
        sql = pd.io.sql.get_schema(self.df, self.name)
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
