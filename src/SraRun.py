import boto3
from io import BytesIO

s3 = boto3.client('s3')

class SraRun(object):

    summary_bucket = 'lovelywater'
    summary_dir = 'summary2'
    summary_suffix = '.summary'
    name = None

    def __init__(self, name):
        self.name = name

    def get_summary(self):
        file_key = f'{self.summary_dir}/{self.name}{self.summary_suffix}'

        with BytesIO() as stream:
            s3.download_fileobj(self.summary_bucket, file_key, stream)
            summary_str = stream.getvalue().decode('UTF-8')
            return summary_str

