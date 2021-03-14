from .. import SummaryBatch
from ..summary.rdrp import RdrpSummary
from ..table.aurora import AuroraTable

class RdrpBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [RdrpSummary(run_id) for run_id in self.run_ids]
        self.tables = {
            'sra': AuroraTable(
                name='rsra',
                cols=['run_id', 'read_length', 'genome', 'aligned_reads', 'date', 'truncated'],
                keys=['run_id']
            ),
            'phy': AuroraTable(
                name='rphylum',
                cols=['run_id', 'phylum_name', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'aligned_length'],
                keys=['run_id', 'phylum_name']
            ),
            'fam': AuroraTable(
                name='rfamily',
                cols=['run_id', 'phylum_name', 'family_name', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'aligned_length'],
                keys=['run_id', 'phylum_name', 'family_name']
            ),
            'vir': AuroraTable(
                name='rdrp',
                cols=['run_id', 'phylum_name', 'family_name', 'virus_name', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'aligned_length'],
                keys=['run_id', 'phylum_name', 'family_name', 'virus_name']
            )
        }
