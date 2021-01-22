import time
from batch.worker_download import get_run_ids
from batch import SummaryBatch

def handler(event, context):
    start_time = time.time()
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    run_ids = list(get_run_ids(start_byte, end_byte))
    summary_batch = SummaryBatch(run_ids)
    summary_batch.process()
    print(summary_batch)
    return

# n = 50
# handler({'start_byte': 0, 'end_byte': n * 10 - 1}, None)
