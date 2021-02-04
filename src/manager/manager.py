import boto3
from lambda_helpers import invoke_lambda
s3 = boto3.resource('s3')

MAX_LINES_PER_WORKER = 1000
MINIMUN_REMAINING_TIME_MS = 10000

class WorkerManager(object):

    def __init__(self, event, context, worker_lambda, index_bucket, index_key):
        self.event = event
        self.context = context
        self.worker_lambda = worker_lambda

        self.start_byte = event.get('start_byte', 0)
        index_object = s3.Object(bucket_name=index_bucket, key=index_key)
        response = index_object.get(Range=f'bytes={self.start_byte}-')
        self.lines = response['Body'].iter_lines()
        self.total_bytes = index_object.content_length

    def process(self):
        worker_start_byte = self.start_byte
        next_start_byte = worker_start_byte
        n_lines = 0
        for line in self.lines:
            n_lines += 1
            next_start_byte += len(line) + 1  # \n
            if n_lines % MAX_LINES_PER_WORKER == 0:
                self.invoke_worker(worker_start_byte, next_start_byte - 1)
                worker_start_byte = next_start_byte
                # check after worker invocation to ensure no overlap or gap
                if self.context.get_remaining_time_in_millis() < MINIMUN_REMAINING_TIME_MS:
                    break

        if next_start_byte < self.total_bytes:
            self.invoke_new_manager(next_start_byte)
        else:
            # final worker
            self.invoke_worker(worker_start_byte, next_start_byte - 1)

        log = {
            'type': self.event['type'],
            'start_byte': self.start_byte,
            'next_start_byte': next_start_byte,
            'n_lines': n_lines
        }
        print(log)
        return log

    def invoke_worker(self, start_byte, end_byte):
        worker_event = {
            'type': self.event['type'],
            'start_byte': start_byte,
            'end_byte': end_byte
        }
        invoke_lambda(self.worker_lambda, worker_event)

    def invoke_new_manager(self, next_start_byte):
        # invoke next manager instance
        next_event = {
            'type': self.event['type'],
            'start_byte': next_start_byte
        }
        invoke_lambda(self.context.function_name, next_event)
