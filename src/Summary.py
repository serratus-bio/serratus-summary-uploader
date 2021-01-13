from summary_download import get_summary_text
from summary_parse import parse_summary
from summary_upload import upload_summary

class Summary(object):

    properties = None
    families = None
    sequences = None
    run_id = None

    def __init__(self, run_id):
        self.run_id = run_id
        summary_text = get_summary_text(run_id)
        parse_summary(self, summary_text)

    def upload(self):
        upload_summary(self)

    def __str__(self):
        return self.run_id
