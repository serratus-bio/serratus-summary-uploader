from .parse import parse_summary

class Summary(object):

    def __init__(self, run_id):
        self.run_id = run_id
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
            raise ValueError(f'Failed to parse {self.run_id}: {e!r}') from e

    def __repr__(self):
        if self.parsed:
            section_info = ''.join(self.sections)
            return f'Summary(sra={self.run_id}, sections={"todo"})'
        return f'Summary(sra={self.run_id})'
