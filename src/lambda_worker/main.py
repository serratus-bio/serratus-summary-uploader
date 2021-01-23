import os
from batch.worker_download import SummaryIndex
from batch.tables import nt_summary_tables
from batch import SummaryBatch

# INDEX_BUCKET = os.environ['INDEX_BUCKET']
# INDEX_FILE = os.environ['INDEX_FILE']
INDEX_BUCKET = 'serratus-athena'
INDEX_FILE = 'index1m.txt'

index = SummaryIndex(INDEX_BUCKET, INDEX_FILE)

def handler(event, context):
    # if (event['clear']):
    #     print('resetting tables and data')
    #     for table in nt_summary_tables.values():
    #         table.delete()
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    sra_ids = list(index.get_sra_ids(start_byte, end_byte))
    summary_batch = SummaryBatch(sra_ids, start_byte)
    summary_batch.parse()
    return

handler({
    'start_byte': 0,
    'end_byte': 49,
    'clear': True
}, None)
