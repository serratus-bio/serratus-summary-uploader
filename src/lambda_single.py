from Summary import Summary

def handler(event, context):
    run_id = event['run']
    print(run_id)
    summary = Summary(run_id)
    if (summary.already_uploaded()):
        return { 'message' : f'{run_id} already processed' }
    summary.upload()
    return { 'message' : f'{run_id} done processing' }
