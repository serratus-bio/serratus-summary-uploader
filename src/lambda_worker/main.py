import os
from batch.download import SummaryIndex
from batch.nucleotide import NucleotideBatch
from batch.protein import ProteinBatch

INDEX_BUCKET = os.environ['INDEX_BUCKET']
NUCLEOTIDE_INDEX = os.environ['NUCLEOTIDE_INDEX']
PROTEIN_INDEX = os.environ['PROTEIN_INDEX']
# INDEX_BUCKET = 'serratus-athena'
# NUCLEOTIDE_INDEX = 'nindex.txt'
# PROTEIN_INDEX = 'pindex.txt'

nucleotide_index = SummaryIndex(INDEX_BUCKET, NUCLEOTIDE_INDEX)
protein_index = SummaryIndex(INDEX_BUCKET, PROTEIN_INDEX)

def handler(event, context):
    if (event['type'] == 'nucleotide'):
        return handler_nucleotide(event, context)
    if (event['type'] == 'protein'):
        return handler_protein(event, context)
    raise ValueError('Invalid type key')

def handler_nucleotide(event, context):
    if (event['clear']):
        print('resetting tables and data')
        for table in NucleotideBatch([], 0).tables.values():
            table.delete_existing()
        return
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    sra_ids = list(nucleotide_index.get_sra_ids(start_byte, end_byte))
    nucleotide_batch = NucleotideBatch(sra_ids, start_byte)
    nucleotide_batch.process()
    return

def handler_protein(event, context):
    if (event['clear']):
        print('resetting tables and data')
        for table in ProteinBatch([], 0).tables.values():
            table.delete_existing()
        return
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    sra_ids = list(protein_index.get_sra_ids(start_byte, end_byte))
    protein_batch = ProteinBatch(sra_ids, start_byte)
    protein_batch.process()
    return
