import time
from Summary import Summary

def handler(event, context):
    start_time = time.time()
    run_id = event['run']
    print(f'[run={run_id}] Starting worker')
    summary = Summary(run_id)
    if (summary.already_uploaded()):
        print(f'[run={run_id}] Already processed. Skipping.')
    summary.process()
    print(f'[run={run_id}] Done processing. Time: {time.time() - start_time}, Families: {len(summary.families)}, Sequences: {len(summary.sequences)}')
    return {
        'run' : run_id,
        'time' : time.time() - start_time,
        'families' : len(summary.families),
        'sequences' : len(summary.sequences)
    }
