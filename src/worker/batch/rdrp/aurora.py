from .. import SummaryBatch
from ..summary.rdrp import RdrpSummary
from ..table.aurora import AuroraTable

class RdrpBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [RdrpSummary(sra_id) for sra_id in self.sra_ids]
        self.tables = {
            'sra': AuroraTable(
                name='rsra',
                cols=['sra_id', 'read_length', 'genome', 'aligned_reads', 'date', 'truncated'],
                keys=['sra_id']
            ),
            'phy': AuroraTable(
                name='rphylum',
                cols=['sra_id', 'phylum_name', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'aligned_length'],
                keys=['sra_id', 'phylum_name']
            ),
            'fam': AuroraTable(
                name='rfamily',
                cols=['sra_id', 'phylum_name', 'family_name', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'aligned_length'],
                keys=['sra_id', 'phylum_name', 'family_name']
            ),
            'vir': AuroraTable(
                name='rdrp',
                cols=['sra_id', 'phylum_name', 'family_name', 'virus_name', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'aligned_length'],
                keys=['sra_id', 'phylum_name', 'family_name', 'virus_name']
            )
        }
