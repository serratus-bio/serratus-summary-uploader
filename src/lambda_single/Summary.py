from summary_download import get_summary_text
from summary_parse import parse_summary
from summary_upload import upload_summary, already_uploaded

class Summary(object):

    properties = {}
    families = []
    sequences = []
    run_id = ''

    def __init__(self, run_id):
        self.run_id = run_id
        summary_text = get_summary_text(run_id)
        try:
            parse_summary(self, summary_text)
        except Exception as e:
            raise ValueError(f'Failed to parse {run_id}: {e}') from e

    def upload(self):
        upload_summary(self)

    def already_uploaded(self):
        return already_uploaded(self.run_id)

    def __str__(self):
        return self.run_id
