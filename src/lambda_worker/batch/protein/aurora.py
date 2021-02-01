from .. import SummaryBatch
from ..summary.protein import ProteinSummary
from ..table.aurora import AuroraTable

class ProteinBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [ProteinSummary(sra_id) for sra_id in self.sra_ids]
        self.tables = {
            'sra': AuroraTable(
                name='psra',
                cols=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date']
            ),
            'fam': AuroraTable(
                name='pfamily',
                cols=['sra', 'fam', 'famcvg', 'score', 'pctid', 'alns', 'avgcols']
            ),
            'gen': AuroraTable(
                name='protein',
                cols=['sra', 'fam', 'protein', 'gencvg', 'score', 'pctid', 'alns', 'avgcols']
            ),
            'seq': AuroraTable(
                name='psequence',
                cols=['sra', 'fam', 'protein', 'seq', 'seqcvg', 'score', 'pctid', 'alns', 'avgcols']
            )
        }
