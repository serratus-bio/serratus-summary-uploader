import boto3
s3 = boto3.resource('s3')

INDEX_BUCKET = 'serratus-athena'
INDEX_FILE = 'index5000.txt'
s3_object = s3.Object(bucket_name=INDEX_BUCKET, key=INDEX_FILE)

def get_run_ids(start_byte, end_byte):
    # assumes start_byte/end_byte are start/end of line
    response = s3_object.get(Range=f'bytes={start_byte}-{end_byte}')
    return (line.decode('utf-8') for line in response['Body'].iter_lines())
