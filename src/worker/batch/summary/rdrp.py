from .file import SummaryFile
from .file_section import SummaryFileSection
from .download import get_summary_file
from botocore.exceptions import ClientError

class RdrpSummary(SummaryFile):

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
        bucket = 'serratus-bio'
        prefix = 'rsummary/'
        suffix = '.psummary'
        try:
            self.set_text(bucket=bucket, prefix=prefix, suffix=suffix)
        except ClientError as e:
            raise RuntimeError(f'[run_id={self.run_id}] {e!r}') from e


class RdrpSummarySraSection(SummaryFileSection):

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


class RdrpSummaryPhySection(SummaryFileSection):

    def __init__(self):
        super().__init__(
            parse_keys=['phycvg', 'phy', 'cat', 'score', 'pctid', 'depth', 'alns', 'avgcols'],
            optional_keys=['cat'],
            name_map = {
                'phycvg': 'coverage_bins',
                'phy': 'phy',  # extend
                'cat': None,
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'alns': 'n_reads',
                'avgcols': 'aligned_length'
            }
        )

    def extend_entry(self, entry):
        entry['phylum_name'] = get_phylum_name(entry['phy'])
        return entry



class RdrpSummaryFamSection(SummaryFileSection):

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
        #   phylum_name=Lenarviricota
        #   family_name=Botourmiaviridae
        #   family_group=Botourmiaviridae-11
        phy_str, fam_str = entry['fam'].split('.')
        entry['phylum_name'] = get_phylum_name(phy_str)
        entry['family_name'], entry['family_group'] = get_family_tuple(fam_str)
        return entry


class RdrpSummaryVirSection(SummaryFileSection):

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
        #   family_name=Totiviridae
        #   family_group=Totiviridae-10
        #   virus_name=phakopsora_totivirus_d
        #   sequence_accession=QED42984
        phy_str, fam_str, vir_str = entry['vir'].split('.', maxsplit=2)
        entry['phylum_name'] = get_phylum_name(phy_str)
        entry['family_name'], entry['family_group'] = get_family_tuple(fam_str)
        entry['virus_name'], entry['sequence_accession'] = vir_str.split(':', maxsplit=1)
        return entry


phylum_name_map = {
    'dupl': 'Duplornaviricota',
    'kiti': 'Kitrinoviricota',
    'levi': 'Lenarviricota',
    'nega': 'Negarnaviricota',
    'pisu': 'Pisuviricota',
    'rdrp': 'Unclassified',
    'var': 'Deltavirus',
}

def get_phylum_name(phy_str):
    '''Return full phylum name'''
    return phylum_name_map[phy_str]


def get_family_tuple(fam_str):
    '''Return family_name, family_group'''
    if fam_str.startswith('Unc'):
        return (fam_str.replace('Unc', 'Unclassified-'), fam_str)
    return (fam_str[:fam_str.index('-')], fam_str)
