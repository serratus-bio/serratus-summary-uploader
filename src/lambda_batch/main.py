import boto3
import json
s3 = boto3.resource('s3')

other_function_name = 'lambda-test'

MINIMUN_REMAINING_TIME_MS = 10000

def handler(event, context):
    bucket = 'serratus-athena'
    index_file = 'index100.txt'
    s3_object = s3.Object(bucket_name=bucket, key=index_file)
    offset = event.get('offset', 0)

    response = s3_object.get(Range=f'bytes={offset}-')

    n_runs_processed = 0
    offset_update = 0
    for line in response['Body'].iter_lines():
        run_id = line.decode('utf-8')
        print(run_id)
        if run_id == '':
            raise ValueError('bad line')
        new_event = { 'run': run_id }
        invoke_lambda(other_function_name, new_event)
        n_runs_processed += 1
        offset_update += len(line) + 1  # \n
        if context.get_remaining_time_in_millis() < MINIMUN_REMAINING_TIME_MS:
            break

    new_offset = offset + offset_update
    if event['continue'] and new_offset < s3_object.content_length:
        new_event = {
            **event,
            'offset': new_offset,
            'continue': True
        }
        invoke_lambda(context.function_name, new_event)
    return {
        'start_offset': offset,
        'next_offset': new_offset,
        'n_runs_processed'  : n_runs_processed
    }

# https://medium.com/swlh/processing-large-s3-files-with-aws-lambda-2c5840ae5c91
def invoke_lambda(function_name, event):
    payload = json.dumps(event).encode('utf-8')
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=payload
    )
