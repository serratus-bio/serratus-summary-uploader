import boto3
import json
import os
s3 = boto3.resource('s3')
lambda_client = boto3.client('lambda')

WORKER_LAMBDA = os.environ['WORKER_LAMBDA']
INDEX_BUCKET = os.environ['INDEX_BUCKET']
INDEX_FILE = os.environ['INDEX_FILE']
MAX_LINES_PER_WORKER = 5000
s3_object = s3.Object(bucket_name=INDEX_BUCKET, key=INDEX_FILE)

def handler(event, context):
    if set(event) <= {'start_byte', 'clear'}:
        return batch_handler(event, context)
    else:
        raise ValueError('Invalid event keys.')

def batch_handler(event, context):
    start_byte = event.get('start_byte', 0)
    clear = event.get('clear', False)
    response = s3_object.get(Range=f'bytes={start_byte}-')
    next_start_byte = start_byte
    n_lines = 0
    for line in response['Body'].iter_lines():
        n_lines += 1
        next_start_byte += len(line) + 1  # \n
        if n_lines >= MAX_LINES_PER_WORKER:
            break

    # invoke worker
    worker_event = {
        'start_byte': start_byte,
        'end_byte': next_start_byte - 1,
        'clear': clear
    }
    invoke_lambda(WORKER_LAMBDA, worker_event)
    
    # invoke next batch
    if next_start_byte < s3_object.content_length:
        invoke_lambda(context.function_name, { 'start_byte': next_start_byte })
    log = {
        'start_byte': start_byte,
        'next_start_byte': next_start_byte,
        'n_lines': n_lines
    }
    print(log)
    return log

# https://medium.com/swlh/processing-large-s3-files-with-aws-lambda-2c5840ae5c91
def invoke_lambda(function_name, event):
    payload = json.dumps(event).encode('utf-8')
    lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=payload
    )
