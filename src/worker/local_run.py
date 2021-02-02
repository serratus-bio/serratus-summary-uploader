import os

os.environ['INDEX_BUCKET'] = 'serratus-athena'
os.environ['NUCLEOTIDE_INDEX'] = 'nindex.txt'
os.environ['PROTEIN_INDEX'] = 'pindex.txt'

from main import handler

handler({
    'type': 'protein',
    'start_byte': 0,
    'end_byte': 49
},
None)

# handler({
#     'type': 'protein',
#     'start_byte': 50,
#     'end_byte': 99
# },
# None)
