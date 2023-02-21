import pandas as pd

class UploadTable(object):

    def __init__(self, name, cols):
        self.name = name
        self.cols = cols
        self.rows = []  # populated by SummaryBatch.parse()
        self.df = None

    def create_dataframe(self):
        if not self.rows:
            return
        self.df = pd.DataFrame(self.rows)[self.cols]

    def upload_init(self):
        pass

    def upload(self):
        pass
