from . import Summary
from .section import SummarySection
from .download import get_protein
from botocore.exceptions import ClientError

class ProteinSummary(Summary):

    def __init__(self, run_id):
        super().__init__(run_id)
        self.line_prefix_ignore = f'sra={run_id};'
        self.sections = {
            'sra': ProteinSraSection(),
            'fam': ProteinFamSection(),
            'gen': ProteinGenSection(),
            'seq': ProteinSeqSection()
        }

    def download(self):
        try:
            self.text = get_protein(self.run_id)
        except ClientError as e:
            raise RuntimeError(f'[run_id={self.run_id}] {e!r}') from e


class ProteinSraSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date'],
            name_map = {
                'sra': 'run_id',
                'type': None,
                'readlength': 'read_length',
                'genome': 'genome',
                'totalalns': 'aligned_reads',
                'truncated': 'truncated',
                'date': 'date'
            },
            is_comment=True
        )


class ProteinFamSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['famcvg', 'fam', 'score', 'pctid', 'alns', 'avgcols'],
            name_map = {
                'famcvg': 'coverage_bins',
                'fam': 'family_name',
                'score': 'score',
                'pctid': 'percent_identity',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )


class ProteinGenSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['gencvg', 'gen', 'score', 'pctid', 'alns', 'avgcols'],
            name_map = {
                'gencvg': 'coverage_bins',
                'gen': 'gen',  # extend
                'score': 'score',
                'pctid': 'percent_identity',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )

    def extend_entry(self, entry):
        # gen=Hugephage.terminase ->
        #   fam=Hugephage
        #   protein=terminase
        entry['family_name'], entry['protein_name'] = entry['gen'].split('.')
        return entry


class ProteinSeqSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['seqcvg', 'seq', 'score', 'pctid', 'alns', 'avgcols'],
            name_map = {
                'seqcvg': 'coverage_bins',
                'seq': 'seq',  # extend
                'score': 'score',
                'pctid': 'percent_identity',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )

    def extend_entry(self, entry):
        # seq=Hugephage.capsid.187.2 ->
        #   fam=Hugephage
        #   protein=capsid
        #   seq=187.2
        entry['family_name'], entry['protein_name'], entry['genbank_id'] = entry['seq'].split('.', maxsplit=2)
        return entry
