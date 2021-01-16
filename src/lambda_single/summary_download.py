import boto3
import io
s3 = boto3.client('s3')

summary_bucket = 'lovelywater'
summary_dir = 'summary2'
summary_suffix = '.summary'

def get_summary_text(run_id):
    file_key = f'{summary_dir}/{run_id}{summary_suffix}'

    with io.BytesIO() as stream:
        s3.download_fileobj(summary_bucket, file_key, stream)
        return stream.getvalue().decode('UTF-8')
