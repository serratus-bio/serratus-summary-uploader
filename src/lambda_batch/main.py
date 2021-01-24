import boto3
import json
import os
s3 = boto3.resource('s3')
lambda_client = boto3.client('lambda')

INDEX_BUCKET = os.environ['INDEX_BUCKET']
NUCLEOTIDE_INDEX = os.environ['NUCLEOTIDE_INDEX']
PROTEIN_INDEX = os.environ['PROTEIN_INDEX']

WORKER_LAMBDA = os.environ['WORKER_LAMBDA']
MAX_LINES_PER_WORKER = 1000
nucleotide_index = s3.Object(bucket_name=INDEX_BUCKET, key=NUCLEOTIDE_INDEX)
protein_index = s3.Object(bucket_name=INDEX_BUCKET, key=PROTEIN_INDEX)

def handler(event, context):
    if (event['type'] == 'nucleotide'):
        return batch_handler(event, context, nucleotide_index)
    if (event['type'] == 'protein'):
        return batch_handler(event, context, protein_index)
    raise ValueError('Invalid type key')

def batch_handler(event, context, index_object):
    start_byte = event.get('start_byte', 0)
    clear = event.get('clear', False)
    response = index_object.get(Range=f'bytes={start_byte}-')
    next_start_byte = start_byte
    n_lines = 0
    for line in response['Body'].iter_lines():
        n_lines += 1
        next_start_byte += len(line) + 1  # \n
        if n_lines >= MAX_LINES_PER_WORKER:
            break

    # invoke worker
    worker_event = {
        'type': event['type'],
        'start_byte': start_byte,
        'end_byte': next_start_byte - 1,
        'clear': clear
    }
    invoke_lambda(WORKER_LAMBDA, worker_event)
    
    # invoke next batch
    if next_start_byte < index_object.content_length:
        next_event = {
            'type': event['type'],
            'start_byte': next_start_byte
        }
        invoke_lambda(context.function_name, next_event)
    log = {
        'type': event['type'],
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
