import time
from summary import Summary
from .worker_upload import (
    upload_runs,
    upload_fams,
    upload_seqs,
    upload_index,
    already_uploaded
)

class SummaryBatch(object):

    def __init__(self, run_ids, log_id):
        self.id = str(hash(tuple(run_ids))).replace('-', '0')
        self.run_ids = run_ids
        self.summary_objects = [Summary(run_id) for run_id in self.run_ids]
        self.log_id = log_id
        self.runs = []
        self.fams = []
        self.seqs = []

    def process(self):
        # self.prune()
        self.parse()
        self.upload_runs()
        self.upload_fams()
        self.upload_seqs()
        self.log(f'Finished {self}')
        # upload_index(self)

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
            self.fams += summary.fams
            self.seqs += summary.seqs
            self.runs.append(summary.props)
        self.log(f'Parsing took {time.time() - start_time:.1f}s')

    def upload_runs(self):
        start_time = time.time()
        self.log('Run upload started')
        upload_runs(self.runs)
        self.log(f'Run upload took {time.time() - start_time:.1f}s')

    def upload_fams(self):
        start_time = time.time()
        self.log('Family upload started')
        upload_fams(self.fams)
        self.log(f'Family upload took {time.time() - start_time:.1f}s')

    def upload_seqs(self):
        start_time = time.time()
        self.log('Sequence upload started')
        upload_seqs(self.seqs)
        self.log(f'Sequence upload took {time.time() - start_time:.1f}s')

    def __repr__(self):
        if self.fams and self.seqs:
            return f'SummaryBatch(runs={len(self.run_ids)}, fams={len(self.fams)}, seqs={len(self.seqs)})'
        return f'SummaryBatch(runs={len(self.run_ids)})'

    def log(self, message):
        print(f'[id={self.log_id}] {message}')
