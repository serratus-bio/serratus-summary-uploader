from .parse import parse_summary
from botocore.exceptions import ClientError

class Summary(object):

    def __init__(self, sra_id):
        self.sra_id = sra_id
        self.text = ''
        self.sections = {}
        self.parsed = False

    def download(self):
        pass

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
