import os
from manager import WorkerManager

INDEX_BUCKET = os.environ['INDEX_BUCKET']
NUCLEOTIDE_INDEX = os.environ['NUCLEOTIDE_INDEX']
PROTEIN_INDEX = os.environ['PROTEIN_INDEX']
WORKER_LAMBDA = os.environ['WORKER_LAMBDA']


def handler(event, context):
    if (event['type'] == 'nucleotide'):
        manager = WorkerManager(event, context, WORKER_LAMBDA, INDEX_BUCKET, NUCLEOTIDE_INDEX)
        return manager.process()
    if (event['type'] == 'protein'):
        manager = WorkerManager(event, context, WORKER_LAMBDA, INDEX_BUCKET, PROTEIN_INDEX)
        return manager.process()
    raise ValueError('Invalid type key')
