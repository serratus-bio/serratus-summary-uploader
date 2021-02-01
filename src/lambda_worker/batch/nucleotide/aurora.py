from .. import SummaryBatch
from ..summary.nucleotide import NucleotideSummary
from ..table.aurora import AuroraTable

class NucleotideBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [NucleotideSummary(sra_id) for sra_id in self.sra_ids]
        self.tables = {
            'sra': AuroraTable(
                name='nsra',
                cols=['sra', 'readlength', 'genome', 'version', 'date'],
                keys=['sra']
            ),
            'fam': AuroraTable(
                name='nfamily',
                cols=['sra', 'fam', 'famcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
                keys=['sra', 'fam']
            ),
            'seq': AuroraTable(
                name='nsequence',
                cols=['sra', 'seq', 'seqcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
                keys=['sra', 'seq']
            )
        }
