import boto3
import io
s3 = boto3.client('s3')

bucket = 'serratus-athena'

nucleotide_dir = 'summary2'
nucleotide_suffix = '.summary'
protein_dir = 'psummary'
protein_suffix = '.psummary'


def get_nucleotide(sra_id):
    file_key = f'{nucleotide_dir}/{sra_id}{nucleotide_suffix}'
    return get_file_contents(file_key)

def get_protein(sra_id):
    file_key = f'{protein_dir}/{sra_id}{protein_suffix}'
    return get_file_contents(file_key)

def get_file_contents(file_key):
    with io.BytesIO() as stream:
        s3.download_fileobj(bucket, file_key, stream)
        return stream.getvalue().decode('UTF-8')
