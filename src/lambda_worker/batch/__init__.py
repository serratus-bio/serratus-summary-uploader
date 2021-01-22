from summary import Summary
from .worker_upload import upload_fams, upload_index, already_uploaded

class SummaryBatch(object):

    id = None
    run_ids = []
    summary_objects = []
    fams = []
    seqs = []

    def __init__(self, run_ids):
        self.id = str(hash(tuple(run_ids))).replace('-', '0')
        self.run_ids = run_ids
        self.summary_objects = [Summary(run_id) for run_id in self.run_ids]

    def process(self):
        # self.prune()
        for summary in self.summary_objects:
            summary.process()
            self.fams += summary.fams
            self.seqs += summary.seqs
        self.upload_fams()
        # upload_index(self)

    def prune(self):
        self.summary_objects = [summary
            for summary in self.summary_objects
            if not already_uploaded(summary)]

    def upload_fams(self):
        upload_fams(self.fams)

    def __repr__(self):
        if self.fams and self.seqs:
            return f'SummaryBatch(runs={len(self.run_ids)}, fams={len(self.fams)}, seqs={len(self.seqs)})'
        return f'SummaryBatch(runs={len(self.run_ids)})'
