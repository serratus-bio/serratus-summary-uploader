import boto3
import io
import os
s3 = boto3.client('s3')

summary_bucket = 'lovelywater'
summary_dir = 'summary2'
summary_suffix = '.summary'
batch_size = 10

def get_summary_text(run_id):
    file_key = f'{summary_dir}/{run_id}{summary_suffix}'

    with io.BytesIO() as stream:
        s3.download_fileobj(summary_bucket, file_key, stream)
        return stream.getvalue().decode('UTF-8')

def get_run_ids():
    response = s3.list_objects_v2(
                    Bucket=summary_bucket,
                    Prefix =summary_dir,
                    MaxKeys=batch_size )
    return [os.path.basename(s3_object['Key']).rstrip(summary_suffix) for s3_object in response['Contents']]
    # TODO: IsTruncated, NextContinuationToken
