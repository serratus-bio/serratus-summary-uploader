from .. import SummaryBatch
from ..summary.nucleotide import NucleotideSummary
from ..table.athena import AthenaTable

class NucleotideBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_files = [NucleotideSummary(run_id) for run_id in self.run_ids]
        s3_dir = 'nucleotide'
        self.tables = {
            'sra': AthenaTable(
                name='nsra',
                cols=['sra', 'readlength', 'genome', 'version', 'date'],
                s3_name='sra',
                s3_dir=s3_dir,
                projection_enabled=False
            ),
            'fam': AthenaTable(
                name='nfamily',
                cols=['sra', 'fam', 'famcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
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
            'seq': AthenaTable(
                name='nsequence',
                cols=['sra', 'seq', 'seqcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
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
