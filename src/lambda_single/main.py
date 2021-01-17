import time
from Summary import Summary

def handler(event, context):
    start_time = time.time()
    run_id = event['run']
    print(run_id)
    summary = Summary(run_id)
    if (summary.already_uploaded()):
        return { 'message' : f'{run_id} already processed' }
    summary.process()
    return {
        'run' : run_id,
        'time' : time.time() - start_time,
        'families' : len(summary.families),
        'sequences' : len(summary.sequences)
    }
