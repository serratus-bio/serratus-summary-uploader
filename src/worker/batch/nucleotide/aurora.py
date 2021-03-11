from .. import SummaryBatch
from ..summary.nucleotide import NucleotideSummary
from ..table.aurora import AuroraTable

class NucleotideBatch(SummaryBatch):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_objects = [NucleotideSummary(run_id) for run_id in self.run_ids]
        self.tables = {
            'sra': AuroraTable(
                name='nsra',
                cols=['run_id', 'read_length', 'genome', 'version', 'date'],
                keys=['run_id']
            ),
            'fam': AuroraTable(
                name='nfamily',
                cols=['run_id', 'family_name', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'n_global_reads', 'length', 'top_genbank_id', 'top_score', 'top_length', 'top_name'],
                keys=['run_id', 'family_name']
            ),
            'seq': AuroraTable(
                name='nsequence',
                cols=['run_id', 'family_name', 'genbank_id', 'coverage_bins', 'score', 'percent_identity', 'depth', 'n_reads', 'n_global_reads', 'length', 'genbank_name'],
                keys=['run_id', 'genbank_id']
            )
        }
