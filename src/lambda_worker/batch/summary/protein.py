from . import Summary
from .section import SummarySection
from .download import get_protein
from botocore.exceptions import ClientError

class ProteinSummary(Summary):

    def __init__(self, sra_id):
        super().__init__(sra_id)
        self.line_prefix_ignore = f'sra={sra_id};'
        self.sections = {
            'sra': SummarySection(
                keys=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date'],
                is_comment=True
            ),
            'fam': SummarySection(
                keys=['famcvg', 'fam', 'score', 'pctid', 'alns', 'avgcols']
            ),
            'gen': SummarySection(
                keys=['gencvg', 'gen', 'score', 'pctid', 'alns', 'avgcols']
            ),
            'seq': SummarySection(
                keys=['seqcvg', 'seq', 'score', 'pctid', 'alns', 'avgcols']
            )
        }

    def download(self):
        try:
            self.text = get_protein(self.sra_id)
        except ClientError as e:
            raise RuntimeError(f'[sra={self.sra_id}] {e!r}') from e
