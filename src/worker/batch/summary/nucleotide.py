from .file import SummaryFile
from .file_section import SummaryFileSection
from botocore.exceptions import ClientError

class NucleotideSummary(SummaryFile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_prefix_ignore = None
        self.sections = {
            'sra': NucleotideSraSection(),
            'fam': NucleotideFamSection(),
            'seq': NucleotideSeqSection()
        }

    def download(self):
        bucket = 'lovelywater'
        prefix = 'summary2/'
        suffix = '.summary'
        try:
            self.set_text(bucket=bucket, prefix=prefix, suffix=suffix)
        except ClientError as e:
            raise RuntimeError(f'[run_id={self.run_id}] {e!r}') from e


class NucleotideSraSection(SummaryFileSection):

    def __init__(self):
        super().__init__(
            parse_keys=['sra', 'readlength', 'genome', 'version', 'date'],
            name_map = {
                'sra': 'run_id',
                'readlength': 'read_length',
                'genome': 'genome',
                'version': 'version',
                'date': 'date'
            },
            is_comment=True
        )


class NucleotideFamSection(SummaryFileSection):

    def __init__(self):
        super().__init__(
            parse_keys=['famcvg', 'fam', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
            name_map = {
                'famcvg': 'coverage_bins',
                'fam': 'family_name',
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'aln': 'n_reads',
                'glb': 'n_global_reads',
                'len': 'length',
                'top': 'top_genbank_id',
                'topscore': 'top_score',
                'toplen': 'top_length',
                'topname': 'top_name'
            },
            last_item_any_char=True
        )


class NucleotideSeqSection(SummaryFileSection):

    def __init__(self):
        super().__init__(
            parse_keys=['seqcvg', 'seq', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
            name_map = {
                'seqcvg': 'coverage_bins',
                'seq': 'sequence_accession',
                'score': 'score',
                'pctid': 'percent_identity',
                'depth': 'depth',
                'aln': 'n_reads',
                'glb': 'n_global_reads',
                'len': 'length',
                'family': 'family_name',
                'name': 'virus_name'
            },
            last_item_any_char=True
        )
