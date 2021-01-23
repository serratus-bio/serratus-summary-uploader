from .summary_download import get_summary_text
from .parse import parse_summary
from botocore.exceptions import ClientError

class Summary(object):

    def __init__(self, sra_id):
        self.sra_id = sra_id
        self.text = ''
        self.sections = {}
        self.parsed = False

    def download(self):
        try:
            self.text = get_summary_text(self.sra_id)
        except ClientError as e:
                raise RuntimeError(f'[sra={self.sra_id}] {e!r}') from e

    def parse(self):
        try:
            parse_summary(self)
            self.parsed = True
        except Exception as e:
            raise ValueError(f'Failed to parse {self.sra_id}: {e!r}') from e

    def __repr__(self):
        if self.parsed:
            section_info = ''.join(self.sections)
            return f'Summary(sra={self.sra_id}, sections={"todo"})'
        return f'Summary(sra={self.sra_id})'
