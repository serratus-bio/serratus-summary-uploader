from . import Summary
from .section import SummarySection

class NucleotideSummary(Summary):

    def __init__(self, *args, **kwargs):
        super(NucleotideSummary, self).__init__(*args, **kwargs)
        self.sections = {
            'fam': SummarySection(
                keys=['famcvg', 'fam', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
                last_item_any_char=True
            ),
            'seq': SummarySection(
                keys=['seqcvg', 'seq', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
                last_item_any_char=True
            )
        }
