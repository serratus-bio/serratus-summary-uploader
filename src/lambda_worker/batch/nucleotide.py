from . import SummaryBatch
from .summary.nucleotide import NucleotideSummary
from .table import UploadTable

class NucleotideBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [NucleotideSummary(sra_id) for sra_id in self.sra_ids]
        s3_dir = 'nucleotide'
        self.tables = {
            'sra': UploadTable(
                name='nsra',
                s3_name='sra',
                s3_dir=s3_dir,
                cols=['sra', 'readlength', 'genome', 'version', 'date'],
                projection_enabled=False
            ),
            'fam': UploadTable(
                name='nfamily',
                s3_name='family',
                s3_dir=s3_dir,
                cols=['sra', 'fam', 'famcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
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
                name='nsequence',
                s3_name='sequence',
                s3_dir=s3_dir,
                cols=['sra', 'seq', 'seqcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
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
