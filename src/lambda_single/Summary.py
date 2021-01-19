from summary_download import get_summary_text
from summary_parse import parse_summary
from summary_upload import upload_summary, already_uploaded

class Summary(object):

    properties = {}
    families = []
    sequences = []
    run_id = ''
    text = ''

    def __init__(self, run_id):
        self.run_id = run_id

    def process(self):
        self.download()
        self.parse()
        self.upload()

    def download(self):
        self.text = get_summary_text(self.run_id)

    def parse(self):
        try:
            parse_summary(self)
        except Exception as e:
            raise ValueError(f'Failed to parse {self.run_id}: {e!r}') from e

    def upload(self):
        upload_summary(self)

    def already_uploaded(self):
        return already_uploaded(self.run_id)

    def __str__(self):
        return self.run_id
