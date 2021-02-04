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
                cols=['sra_id', 'read_length', 'genome', 'aligned_reads', 'date', 'truncated'],
                keys=['sra_id']
            ),
            'fam': AuroraTable(
                name='pfamily',
                cols=['sra_id', 'family_name', 'coverage_bins', 'score', 'percent_identity', 'n_reads', 'aligned_length'],
                keys=['sra_id', 'family_name']
            ),
            'gen': AuroraTable(
                name='protein',
                cols=['sra_id', 'family_name', 'protein_name', 'coverage_bins', 'score', 'percent_identity', 'n_reads', 'aligned_length'],
                keys=['sra_id', 'family_name', 'protein_name']
            ),
            'seq': AuroraTable(
                name='psequence',
                cols=['sra_id', 'family_name', 'protein_name', 'genbank_id', 'coverage_bins', 'score', 'percent_identity', 'n_reads', 'aligned_length'],
                keys=['sra_id', 'family_name', 'protein_name', 'genbank_id']
            )
        }
