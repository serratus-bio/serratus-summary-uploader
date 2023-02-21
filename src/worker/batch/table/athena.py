from . import UploadTable
import awswrangler as wr

upload_bucket = 'serratus-athena'
athena_database = 'summary'
parquet_mode = 'append'

class AthenaTable(UploadTable):

    def __init__(self, name, s3_name, s3_dir, cols, projection_enabled=False, projection_types=None, projection_ranges=None):
        super().__init__(name, cols)
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

    def upload_init(self):
        # Athena doesn't need any initialization
        pass

    def upload(self):
        if not self.rows:
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

    def upload_teardown(self):
        wr.catalog.delete_table_if_exists(database=athena_database, table=self.name)
        wr.s3.delete_objects(self.s3_path)
