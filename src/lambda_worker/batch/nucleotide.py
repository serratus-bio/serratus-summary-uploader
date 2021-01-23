from . import SummaryBatch
from .summary.nucleotide import NucleotideSummary
from .uploadtable import UploadTable

class NucleotideBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super(NucleotideBatch, self).__init__(*args, **kwargs)
        self.summary_objects = [NucleotideSummary(sra_id) for sra_id in self.sra_ids]
        self.tables = {
            'sra': UploadTable(
                name='sra4',
                cols=['sra', 'readlength', 'genome', 'version', 'date'],
                projection_enabled=False
            ),
            'fam': UploadTable(
                name='fam4',
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
                name='seq4',
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

    def __repr__(self):
        if self.processed:
            return f'SummaryBatch(sras={len(self.sra_ids)}, fams={len(self.tables["fam"].entries)}, seqs={len(self.tables["seq"].entries)})'
        return f'SummaryBatch(sras={len(self.sra_ids)})'
