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
            self.tables['fam'].entries += summary.sections['fam'].entries
            self.tables['seq'].entries += summary.sections['seq'].entries
            self.tables['sra'].entries.append(summary.props)
        self.log(f'Parsing took {time.time() - start_time:.1f}s')

    def upload(self):
        for table in self.tables.values():
            start_time = time.time()
            self.log(f'Table {table.name} upload started')
            table.upload()
            self.log(f'Table {table.name} upload took {time.time() - start_time:.1f}s')

    def __repr__(self):
        if self.processed:
            return f'SummaryBatch(sras={len(self.sra_ids)}, fams={len(self.tables["fam"].entries)}, seqs={len(self.tables["seq"].entries)})'
        return f'SummaryBatch(sras={len(self.sra_ids)})'

    def log(self, message):
        print(f'[id={self.log_id}] {message}')
