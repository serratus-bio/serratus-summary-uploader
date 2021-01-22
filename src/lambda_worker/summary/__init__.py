from .summary_download import get_summary_text
from .summary_parse import parse_summary

class Summary(object):

    properties = {}
    fams = []
    seqs = []
    run_id = ''
    text = ''

    def __init__(self, run_id):
        self.run_id = run_id

    def process(self):
        self.download()
        self.parse()

    def download(self):
        self.text = get_summary_text(self.run_id)

    def parse(self):
        try:
            parse_summary(self)
        except Exception as e:
            raise ValueError(f'Failed to parse {self.run_id}: {e!r}') from e

    def __repr__(self):
        if self.fams and self.seqs:
            return f'Summary(run={self.run_id}, fams={len(self.fams)}, seqs={len(self.seqs)})'
        return f'Summary(run={self.run_id})'
