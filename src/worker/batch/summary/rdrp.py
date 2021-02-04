from . import Summary
from .section import SummarySection
from .download import get_rdrp
from botocore.exceptions import ClientError

class RdrpSummary(Summary):

    def __init__(self, sra_id):
        super().__init__(sra_id)
        self.line_prefix_ignore = f'sra={sra_id};'
        self.sections = {
            'sra': RdrpSummarySraSection(),
            'phy': RdrpSummaryPhySection(),
            'fam': RdrpSummaryFamSection(),
            'vir': RdrpSummaryVirSection()
        }

    def download(self):
        try:
            self.text = get_rdrp(self.sra_id)
        except ClientError as e:
            raise RuntimeError(f'[sra={self.sra_id}] {e!r}') from e


class RdrpSummarySraSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['sra', 'type', 'readlength', 'genome', 'totalalns', 'truncated', 'date'],
            name_map = {
                'sra': 'sra_id',
                'type': None,
                'readlength': 'read_length',
                'genome': 'genome',
                'totalalns': 'aligned_reads',
                'truncated': None,
                'date': 'date'
            },
            is_comment=True
        )


class RdrpSummaryPhySection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['phycvg', 'phy', 'score', 'pctid', 'depth', 'alns', 'avgcols'],
            name_map = {
                'phycvg': 'coverage_bins',
                'phy': 'phylum_name',
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
            parse_keys=['famcvg', 'fam', 'score', 'pctid', 'depth', 'alns', 'avgcols'],
            name_map = {
                'famcvg': 'coverage_bins',
                'fam': 'fam',  # expand
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )

    def expand_entry(self, entry):
        # fam=levi.Botourmiaviridae-11 ->
        #   phylum_name=levi
        #   family_name=Botourmiaviridae-11
        entry['phylum_name'], entry['family_name'] = entry['fam'].split('.')
        return entry


class RdrpSummaryVirSection(SummarySection):

    def __init__(self):
        super().__init__(
            parse_keys=['vircvg', 'vir', 'score', 'pctid', 'depth', 'alns', 'avgcols'],
            name_map = {
                'vircvg': 'coverage_bins',
                'vir': 'vir',  # expand
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )

    def expand_entry(self, entry):
        # vir=dupl.Totiviridae-10.phakopsora_totivirus_d:QED42984 ->
        #   phylum_name=dupl
        #   family_name=Totiviridae-10
        #   virus_name=phakopsora_totivirus_d:QED42984
        entry['phylum_name'], entry['family_name'], entry['virus_name'] = entry['vir'].split('.', maxsplit=2)
        return entry
