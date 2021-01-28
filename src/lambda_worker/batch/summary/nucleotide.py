from . import Summary
from .section import SummarySection
from .download import get_nucleotide
from botocore.exceptions import ClientError

class NucleotideSummary(Summary):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_prefix_ignore = None
        self.sections = {
            'sra': SummarySection(
                parse_keys=['sra', 'readlength', 'genome', 'version', 'date'],
                is_comment=True
            ),
            'fam': SummarySection(
                parse_keys=['famcvg', 'fam', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
                last_item_any_char=True
            ),
            'seq': SummarySection(
                parse_keys=['seqcvg', 'seq', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
                last_item_any_char=True
            )
        }

    def download(self):
        try:
            self.text = get_nucleotide(self.sra_id)
        except ClientError as e:
            raise RuntimeError(f'[sra={self.sra_id}] {e!r}') from e
