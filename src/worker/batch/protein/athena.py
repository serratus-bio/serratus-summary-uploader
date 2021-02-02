from .. import SummaryBatch
from ..summary.protein import ProteinSummary
from ..table.athena import AthenaTable

class ProteinBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [ProteinSummary(sra_id) for sra_id in self.sra_ids]
        s3_dir = 'protein'
        self.tables = {
            'sra': AthenaTable(
                name='psra',
                cols=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date'],
                s3_name='sra',
                s3_dir=s3_dir,
                projection_enabled=False
            ),
            'fam': AthenaTable(
                name='pfamily',
                cols=['sra', 'fam', 'famcvg', 'score', 'pctid', 'alns', 'avgcols'],
                s3_name='family',
                s3_dir=s3_dir,
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
            'gen': AthenaTable(
                name='protein',
                cols=['sra', 'fam', 'protein', 'gencvg', 'score', 'pctid', 'alns', 'avgcols'],
                s3_name='protein',
                s3_dir=s3_dir,
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
            'seq': AthenaTable(
                name='psequence',
                cols=['sra', 'fam', 'protein', 'seq', 'seqcvg', 'score', 'pctid', 'alns', 'avgcols'],
                s3_name='sequence',
                s3_dir=s3_dir,
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
