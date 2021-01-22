import boto3
s3 = boto3.resource('s3')

class SummaryIndex(object):

    def __init__(self, bucket, path):
        self.s3_object = s3.Object(bucket_name=bucket, key=path)

    def get_run_ids(self, start_byte, end_byte):
        # assumes start_byte/end_byte are start/end of line
        response = self.s3_object.get(Range=f'bytes={start_byte}-{end_byte}')
        return (line.decode('utf-8') for line in response['Body'].iter_lines())
