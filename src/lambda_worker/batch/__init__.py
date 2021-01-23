import time
from summary import Summary
from .tables import nt_summary_tables

class SummaryBatch(object):

    def __init__(self, run_ids, log_id):
        self.run_ids = run_ids
        self.summary_objects = [Summary(run_id) for run_id in self.run_ids]
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

    def prune(self):
        self.summary_objects = [summary
            for summary in self.summary_objects
            if not already_uploaded(summary)]

    def parse(self):
        start_time = time.time()
        self.log('Parsing started')
        for summary in self.summary_objects:
            summary.download()
            summary.parse()
            self.tables['fam'].entries += summary.fams
            self.tables['seq'].entries += summary.seqs
            self.tables['run'].entries.append(summary.props)
        self.log(f'Parsing took {time.time() - start_time:.1f}s')

    def __repr__(self):
        if self.processed:
            return f'SummaryBatch(runs={len(self.run_ids)}, fams={len(self.tables["fam"].entries)}, seqs={len(self.tables["seq"].entries)})'
        return f'SummaryBatch(runs={len(self.run_ids)})'

    def log(self, message):
        print(f'[id={self.log_id}] {message}')
