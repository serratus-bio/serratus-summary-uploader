from .uploadtable import UploadTable

nt_summary_tables = {
    'sra': UploadTable(
        name='sra4',
        cols=['sra', 'readlength', 'genome', 'version', 'date'],
        projection_enabled=False
    ),
    'fam': UploadTable(
        name='fam4',
        cols=['sra', 'fam', 'famcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'],
        projection_enabled=True,
        projection_types={
            'score': 'integer',
            'pctid':'integer'
        },
        projection_ranges={
            'score': '0,100',
            'pctid':'0,100'
        }
    ),
    'seq': UploadTable(
        name='seq4',
        cols=['sra', 'seq', 'seqcvg', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'],
        projection_enabled=True,
        projection_types={
            'score': 'integer',
            'pctid':'integer'
        },
        projection_ranges={
            'score': '0,100',
            'pctid':'0,100'
        }
    )
}