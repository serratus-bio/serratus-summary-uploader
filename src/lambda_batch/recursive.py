import boto3
import json
import os
from main import (
    s3,
    s3_object,
    lambda_client,
    invoke_lambda,
    WORKER_LAMBDA
)

recursive_event_keys = {
    'start_byte',
    'end_byte'
}

# Recursive (divide-and-conquer) method of processing an index file.
# Bottleneck: s3_object.get
def recursive_batch(event, context):
    start_byte = event.get('start_byte', 0)
    end_byte = event.get('end_byte', s3_object.content_length)
    if (start_byte == end_byte):
        return
    response = s3_object.get(Range=f'bytes={start_byte}-{end_byte}')

    lines = response['Body'].iter_lines()
    line = next(lines)
    single_line = False
    try:
        next(lines)
    except Exception:
        single_line = True

    if (single_line):
        run_id = line.decode('utf-8')
        new_event = { 'run': run_id }
        print(run_id)
        invoke_lambda(WORKER_LAMBDA, new_event)

    mid_byte = get_mid_byte(start_byte, end_byte)

    event1 = {
        'start_byte': start_byte,
        'end_byte': mid_byte - 1
    }
    invoke_lambda(context.function_name, event1)

    event2 = {
        'start_byte': mid_byte,
        'end_byte': end_byte
    }
    invoke_lambda(context.function_name, event2)

    return {
        'content_length': s3_object.content_length,
        'start_byte': start_byte,
        'mid_byte': mid_byte,
        'end_byte': end_byte
    }

def get_mid_byte(start_byte, end_byte):
    mid_byte = (start_byte + end_byte) // 2
    response = s3_object.get(Range=f'bytes={mid_byte}-{end_byte}')
    chunk_size = 1024
    chunks = response['Body'].iter_chunks(chunk_size)
    i_newline = 0
    for chunk in chunks:
        try:
            i_newline += chunk.index(bytes(b'\n'))
            break
        except ValueError:
            i_newline += chunk_size
            continue
    mid_byte += i_newline + 1
    return mid_byte
