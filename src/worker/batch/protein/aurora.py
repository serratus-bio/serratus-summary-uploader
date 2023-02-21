from .. import SummaryBatch
from ..summary.protein import ProteinSummary
from ..table.aurora import AuroraTable

class ProteinBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_files = [ProteinSummary(run_id) for run_id in self.run_ids]
        self.tables = {
            'sra': AuroraTable(
                name='psra',
                cols=['run_id', 'read_length', 'genome', 'aligned_reads', 'date', 'truncated'],
                keys=['run_id']
            ),
            'fam': AuroraTable(
                name='pfamily',
                cols=['run_id', 'family_name', 'coverage_bins', 'score', 'percent_identity', 'n_reads', 'aligned_length'],
                keys=['run_id', 'family_name']
            ),
            'gen': AuroraTable(
                name='protein',
                cols=['run_id', 'family_name', 'protein_name', 'coverage_bins', 'score', 'percent_identity', 'n_reads', 'aligned_length'],
                keys=['run_id', 'family_name', 'protein_name']
            ),
            'seq': AuroraTable(
                name='psequence',
                cols=['run_id', 'family_name', 'protein_name', 'genbank_id', 'coverage_bins', 'score', 'percent_identity', 'n_reads', 'aligned_length'],
                keys=['run_id', 'family_name', 'protein_name', 'genbank_id']
            )
        }
