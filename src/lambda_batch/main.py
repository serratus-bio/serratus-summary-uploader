import boto3
import json
import os
s3 = boto3.resource('s3')
lambda_client = boto3.client('lambda')

WORKER_LAMBDA = os.environ['WORKER_LAMBDA']
INDEX_BUCKET = os.environ['INDEX_BUCKET']
INDEX_FILE = os.environ['INDEX_FILE']
MINIMUN_REMAINING_TIME_MS = 10000
MAX_LINES_PER_BRANCH = 1000
s3_object = s3.Object(bucket_name=INDEX_BUCKET, key=INDEX_FILE)

seed_event_keys = {
    'start_byte'
}

branch_event_keys = {
    'start_byte',
    'end_byte'
}

def handler(event, context):
    if set(event) <= seed_event_keys:
        return seed_handler(event, context)
    if set(event) == branch_event_keys:
        return branch_handler(event, context)
    else:
        raise ValueError('Invalid event keys.')

def seed_handler(event, context):
    start_byte = event.get('start_byte', 0)
    response = s3_object.get(Range=f'bytes={start_byte}-')
    next_start_byte = start_byte
    n_lines = 0
    for line in response['Body'].iter_lines():
        run_id = line.decode('utf-8')
        n_lines += 1
        next_start_byte += len(line) + 1  # \n
        if n_lines >= MAX_LINES_PER_BRANCH:
            break
        if context.get_remaining_time_in_millis() < MINIMUN_REMAINING_TIME_MS:
            break

    # invoke branch
    invoke_lambda(context.function_name, { 'start_byte': start_byte, 'end_byte': next_start_byte - 1 })
    if next_start_byte < s3_object.content_length:
        invoke_lambda(context.function_name, { 'start_byte': next_start_byte })
    log = {
        'n_lines': n_lines
    }
    print(log)
    return log

def branch_handler(event, context):
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    response = s3_object.get(Range=f'bytes={start_byte}-{end_byte}')
    n_workers_invoked = 0
    next_start_byte = start_byte
    for line in response['Body'].iter_lines():
        run_id = line.decode('utf-8')
        if run_id == '':
            raise ValueError('bad line')
        new_event = { 'run': run_id }
        invoke_lambda(WORKER_LAMBDA, new_event)
        n_workers_invoked += 1
        next_start_byte += len(line) + 1  # \n
        if context.get_remaining_time_in_millis() < MINIMUN_REMAINING_TIME_MS:
            break

    if next_start_byte < end_byte:
        invoke_lambda(context.function_name, { 'start_byte': next_start_byte, 'end_byte': end_byte })
    log = {
        'start_byte': start_byte,
        'end_byte': end_byte,
        'next_start_byte': next_start_byte,
        'n_workers_invoked'  : n_workers_invoked
    }
    print(log)

# https://medium.com/swlh/processing-large-s3-files-with-aws-lambda-2c5840ae5c91
def invoke_lambda(function_name, event):
    payload = json.dumps(event).encode('utf-8')
    lambda_response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=payload
    )
