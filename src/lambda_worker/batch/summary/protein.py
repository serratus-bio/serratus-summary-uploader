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
                parse_keys=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date'],
                is_comment=True
            ),
            'fam': ProteinFamSection(),
            'gen': ProteinGenSection(),
            'seq': ProteinSeqSection()
        }

    def download(self):
        try:
            self.text = get_protein(self.sra_id)
        except ClientError as e:
            raise RuntimeError(f'[sra={self.sra_id}] {e!r}') from e

class ProteinFamSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['famcvg', 'fam', 'score', 'pctid', 'alns', 'avgcols']
        )

    def expand_entries(self):
        for entry in self.entries:
            entry['pkey']= f"{entry['fam']}_{entry['sra']}"

class ProteinGenSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['gencvg', 'gen', 'score', 'pctid', 'alns', 'avgcols']
        )

    def expand_entries(self):
        # gen=Hugephage.terminase ->
        #   fam=Hugephage
        #   protein=terminase
        for entry in self.entries:
            entry['pkey']= f"{entry['gen']}_{entry['sra']}"
            entry['fam'], entry['protein'] = entry['gen'].split('.')


class ProteinSeqSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['seqcvg', 'seq', 'score', 'pctid', 'alns', 'avgcols']
        )

    def expand_entries(self):
        # seq=Hugephage.capsid.187 ->
        #   fam=Hugephage
        #   protein=capsid
        #   seq=187
        for entry in self.entries:
            entry['pkey']= f"{entry['seq']}_{entry['sra']}"
            # allow '.' in seq
            entry['fam'], entry['protein'], entry['seq'] = entry['seq'].split('.', maxsplit=2)
