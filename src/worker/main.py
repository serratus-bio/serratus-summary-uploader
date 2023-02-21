import os
from typing import TypedDict
from batch.download import SummaryIndex
from batch.nucleotide.aurora import NucleotideBatch
from batch.protein.aurora import ProteinBatch
from batch.rdrp.aurora import RdrpBatch


# S3 bucket containing index files.
INDEX_BUCKET = os.environ['INDEX_BUCKET']

# Index file for nucleotide search.
NUCLEOTIDE_INDEX = os.environ['NUCLEOTIDE_INDEX']

# Index file for protein search.
PROTEIN_INDEX = os.environ['PROTEIN_INDEX']

# Index file for rdrp search.
RDRP_INDEX = os.environ['RDRP_INDEX']


nucleotide_index = SummaryIndex(INDEX_BUCKET, NUCLEOTIDE_INDEX)
protein_index = SummaryIndex(INDEX_BUCKET, PROTEIN_INDEX)
rdrp_index = SummaryIndex(INDEX_BUCKET, RDRP_INDEX)


class LambdaHandlerEvent(TypedDict):
    # Which Serratus search result to upload.
    type: str

    # Start byte of index file to seek from.
    start_byte: int

    # End byte of index file to seek to.
    end_byte: int


def handler(event: LambdaHandlerEvent, context):
    if (event['type'] == 'nucleotide'):
        return handler_nucleotide(event, context)
    if (event['type'] == 'protein'):
        return handler_protein(event, context)
    if (event['type'] == 'rdrp'):
        return handler_rdrp(event, context)
    raise ValueError('Invalid type key')


def handler_nucleotide(event: LambdaHandlerEvent, context):
    if (event.get('clear', False)):
        print('resetting tables and data')
        for table in NucleotideBatch([], 0).tables.values():
            table.upload_teardown()
        return
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    run_ids = list(nucleotide_index.get_run_ids(start_byte, end_byte))
    nucleotide_batch = NucleotideBatch(run_ids, start_byte)
    nucleotide_batch.process()
    return


def handler_protein(event: LambdaHandlerEvent, context):
    if (event.get('clear', False)):
        print('resetting tables and data')
        for table in ProteinBatch([], 0).tables.values():
            table.upload_teardown()
        return
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    run_ids = list(protein_index.get_run_ids(start_byte, end_byte))
    protein_batch = ProteinBatch(run_ids, start_byte)
    protein_batch.process()
    return


def handler_rdrp(event: LambdaHandlerEvent, context):
    if (event.get('clear', False)):
        print('resetting tables and data')
        for table in RdrpBatch([], 0).tables.values():
            table.upload_teardown()
        return
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    run_ids = list(rdrp_index.get_run_ids(start_byte, end_byte))
    rdrp_batch = RdrpBatch(run_ids, start_byte)
    rdrp_batch.process()
    return
