import time
from summary.ntsummary import NTSummary
from .tables import nt_summary_tables

class SummaryBatch(object):

    def __init__(self, sra_ids, log_id):
        self.sra_ids = sra_ids
        self.summary_objects = [NTSummary(sra_id) for sra_id in self.sra_ids]
        self.log_id = log_id
        self.tables = nt_summary_tables
        self.processed = False

    def process(self):
        self.parse()
        for table in self.tables.values():
            start_time = time.time()
            self.log(f'Table {table.name} upload started')
            table.upload()
            self.log(f'Table {table.name} upload took {time.time() - start_time:.1f}s')
        self.processed = True
        self.log(f'Finished {self}')

    def parse(self):
        start_time = time.time()
        self.log('Parsing started')
        for summary in self.summary_objects:
            summary.download()
            summary.parse()
            self.tables['fam'].entries += summary.sections['fam'].entries
            self.tables['seq'].entries += summary.sections['seq'].entries
            self.tables['sra'].entries.append(summary.props)
        self.log(f'Parsing took {time.time() - start_time:.1f}s')

    def __repr__(self):
        if self.processed:
            return f'SummaryBatch(sras={len(self.sra_ids)}, fams={len(self.tables["fam"].entries)}, seqs={len(self.tables["seq"].entries)})'
        return f'SummaryBatch(sras={len(self.sra_ids)})'

    def log(self, message):
        print(f'[id={self.log_id}] {message}')
