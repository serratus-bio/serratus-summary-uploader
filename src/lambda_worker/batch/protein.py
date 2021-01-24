from . import SummaryBatch
from .summary.protein import ProteinSummary
from .table import UploadTable

class ProteinBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [ProteinSummary(sra_id) for sra_id in self.sra_ids]
        self.tables = {
            'sra': UploadTable(
                name='psra',
                cols=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date'],
                projection_enabled=False
            ),
            'fam': UploadTable(
                name='pfamily',
                cols=['fam', 'famcvg', 'score', 'pctid', 'alns', 'avgcols'],
                projection_enabled=True,
                projection_types={
                    'score': 'integer',
                    'pctid':'integer'
                },
                projection_ranges={
                    'score': '0,100',
                    'pctid':'0,100'
                }
            ),
            'gen': UploadTable(
                name='protein',
                cols=['gen', 'gencvg', 'score', 'pctid', 'alns', 'avgcols'],
                projection_enabled=True,
                projection_types={
                    'score': 'integer',
                    'pctid':'integer'
                },
                projection_ranges={
                    'score': '0,100',
                    'pctid':'0,100'
                }
            ),
            'seq': UploadTable(
                name='psequence',
                cols=['seq', 'seqcvg', 'score', 'pctid', 'alns', 'avgcols'],
                projection_enabled=True,
                projection_types={
                    'score': 'integer',
                    'pctid':'integer'
                },
                projection_ranges={
                    'score': '0,100',
                    'pctid':'0,100'
                }
            )
        }
