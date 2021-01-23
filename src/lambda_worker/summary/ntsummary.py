from . import Summary
from .section import SummarySection

class NTSummary(Summary):

    def __init__(self, *args, **kwargs):
        super(NTSummary, self).__init__(*args, **kwargs)
        self.sections = {
            'fam': SummarySection(
                name='family',
                keys=['famcvg', 'fam', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
                add_sra=True,
                last_item_any_char=True
            ),
            'seq': SummarySection(
                name='sequence',
                keys=['seqcvg', 'seq', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
                add_sra=True,
                last_item_any_char=True
            )
        }
