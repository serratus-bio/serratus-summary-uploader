import awswrangler as wr
import pandas as pd

upload_bucket = 'serratus-athena'
athena_database = 'summary'
parquet_mode = 'append'

class UploadTable(object):

    def __init__(self, name, cols, projection_enabled=False, projection_types=None, projection_ranges=None):
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

    def upload(self):
        wr.s3.to_parquet(
            df=pd.DataFrame(self.entries)[self.cols],
            path=f"s3://{upload_bucket}/{self.name}/",
            dataset=True,
            mode=parquet_mode,
            database=athena_database,
            table=self.name,
            **self.projection_kwargs
        )

    def delete(self):
        wr.catalog.delete_table_if_exists(database=athena_database, table=self.name)
        wr.s3.delete_objects(f's3://{upload_bucket}/{self.name}')
