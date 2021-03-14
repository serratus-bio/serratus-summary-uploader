from . import Summary
from .section import SummarySection
from .download import get_rdrp
from botocore.exceptions import ClientError

class RdrpSummary(Summary):

    def __init__(self, run_id):
        super().__init__(run_id)
        self.line_prefix_ignore = f'sra={run_id};'
        self.sections = {
            'sra': RdrpSummarySraSection(),
            'phy': RdrpSummaryPhySection(),
            'fam': RdrpSummaryFamSection(),
            'vir': RdrpSummaryVirSection()
        }

    def download(self):
        try:
            self.text = get_rdrp(self.run_id)
        except ClientError as e:
            raise RuntimeError(f'[run_id={self.run_id}] {e!r}') from e


class RdrpSummarySraSection(SummarySection):

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


class RdrpSummaryPhySection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['phycvg', 'phy', 'cat', 'score', 'pctid', 'depth', 'alns', 'avgcols'],
            optional_keys=['cat'],
            name_map = {
                'phycvg': 'coverage_bins',
                'phy': 'phylum_name',
                'cat': None,
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )


class RdrpSummaryFamSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['famcvg', 'fam', 'cat', 'score', 'pctid', 'depth', 'alns', 'avgcols'],
            optional_keys=['cat'],
            name_map = {
                'famcvg': 'coverage_bins',
                'fam': 'fam',  # extend
                'cat': None,
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )

    def extend_entry(self, entry):
        # fam=levi.Botourmiaviridae-11 ->
        #   phylum_name=levi
        #   family_name=Botourmiaviridae-11
        entry['phylum_name'], entry['family_name'] = entry['fam'].split('.')
        return entry


class RdrpSummaryVirSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['vircvg', 'vir', 'cat', 'score', 'pctid', 'depth', 'alns', 'avgcols'],
            optional_keys=['cat'],
            name_map = {
                'vircvg': 'coverage_bins',
                'vir': 'vir',  # extend
                'cat': None,
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )

    def extend_entry(self, entry):
        # vir=dupl.Totiviridae-10.phakopsora_totivirus_d:QED42984 ->
        #   phylum_name=dupl
        #   family_name=Totiviridae-10
        #   virus_name=phakopsora_totivirus_d:QED42984
        entry['phylum_name'], entry['family_name'], entry['virus_name'] = entry['vir'].split('.', maxsplit=2)
        return entry
