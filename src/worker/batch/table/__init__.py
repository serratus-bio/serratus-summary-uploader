import pandas as pd

class UploadTable(object):

    def __init__(self, name, cols):
        self.name = name
        self.cols = cols
        self.entries = []  # populated by SummaryBatch.parse()

    def create_dataframe(self):
        if not self.entries:
            return
        self.df = pd.DataFrame(self.entries)[self.cols]
