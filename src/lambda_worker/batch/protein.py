from . import SummaryBatch
from .summary.protein import ProteinSummary
from .table import UploadTable

class ProteinBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [ProteinSummary(sra_id) for sra_id in self.sra_ids]
        s3_dir = 'protein'
        self.tables = {
            'sra': UploadTable(
                name='psra',
                s3_name='sra',
                s3_dir=s3_dir,
                cols=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date'],
                partition_key='sra',
                projection_enabled=False
            ),
            'fam': UploadTable(
                name='pfamily',
                s3_name='family',
                s3_dir=s3_dir,
                cols=['pkey', 'sra', 'fam', 'famcvg', 'score', 'pctid', 'alns', 'avgcols'],
                partition_key='pkey',
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
                s3_name='protein',
                s3_dir=s3_dir,
                cols=['pkey', 'sra', 'fam', 'protein', 'gencvg', 'score', 'pctid', 'alns', 'avgcols'],
                partition_key='pkey',
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
                s3_name='sequence',
                s3_dir=s3_dir,
                cols=['pkey', 'sra', 'fam', 'protein', 'seq', 'seqcvg', 'score', 'pctid', 'alns', 'avgcols'],
                partition_key='pkey',
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
