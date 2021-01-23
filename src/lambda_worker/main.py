import os
from batch.download import SummaryIndex
from batch.nucleotide import NucleotideBatch

# INDEX_BUCKET = os.environ['INDEX_BUCKET']
# INDEX_FILE = os.environ['INDEX_FILE']
INDEX_BUCKET = 'serratus-athena'
INDEX_FILE = 'index1m.txt'

index = SummaryIndex(INDEX_BUCKET, INDEX_FILE)

def handler(event, context):
    if (event['clear']):
        print('resetting tables and data')
        for table in NucleotideBatch([], 0).tables.values():
            table.delete_existing()
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    sra_ids = list(index.get_sra_ids(start_byte, end_byte))
    summary_batch = NucleotideBatch(sra_ids, start_byte)
    summary_batch.process()
    return

handler({
    'start_byte': 0,
    'end_byte': 49,
    'clear': True
}, None)
