import time

class SummaryBatch(object):

    def __init__(self, sra_ids, log_id):
        self.sra_ids = sra_ids
        self.log_id = log_id
        self.processed = False
        self.summary_objects = []
        self.tables = {}

    def process(self):
        self.download()
        self.parse()
        self.create_dataframe()
        # self.create_dynamodb_table()
        self.upload()
        self.processed = True
        self.log(f'Finished {self}')

    def download(self):
        start_time = time.time()
        self.log('Download started')
        for summary in self.summary_objects:
            summary.download()
        self.log(f'Download took {time.time() - start_time:.1f}s')

    def parse(self):
        start_time = time.time()
        self.log('Parsing started')
        for summary in self.summary_objects:
            summary.parse()
            for key, table in self.tables.items():
                table.entries += summary.sections[key].entries
        self.log(f'Parsing took {time.time() - start_time:.1f}s')

    def create_dataframe(self):
        start_time = time.time()
        self.log(f'Dataframe creation started')
        for table in self.tables.values():
            table.create_dataframe()
        self.log(f'Dataframe creation took {time.time() - start_time:.1f}s')

    def create_dynamodb_table(self):
        start_time = time.time()
        self.log(f'Dynamodb table creation started')
        for table in self.tables.values():
            table.create_dynamodb_table()
        self.log(f'Dynamodb table creation took {time.time() - start_time:.1f}s')

    def upload(self):
        for table in self.tables.values():
            start_time = time.time()
            self.log(f'Table {table.name} upload started')
            table.upload_dynamodb()
            self.log(f'Table {table.name} upload took {time.time() - start_time:.1f}s')

    def __repr__(self):
        if self.processed:
            table_info = ','.join(
                f'{key}={len(table.entries)}'
                for key, table in self.tables.items()
            )
            return f'{self.__class__.__name__}({table_info})'
        return f'{self.__class__.__name__}()'

    def log(self, message):
        print(f'[id={self.log_id}] {message}')
