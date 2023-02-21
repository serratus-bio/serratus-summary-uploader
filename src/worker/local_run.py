# The worker is designed to run on AWS Lambda, but this file can be used to run
# the worker locally for testing purposes.

import os

os.environ['INDEX_BUCKET'] = 'serratus-summary-uploader'
os.environ['NUCLEOTIDE_INDEX'] = 'nindex.txt'
os.environ['PROTEIN_INDEX'] = 'pindex.txt'
os.environ['RDRP_INDEX'] = 'rindex.txt'

from main import handler

handler({
    'type': 'rdrp',
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
