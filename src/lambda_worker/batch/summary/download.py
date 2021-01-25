import urllib

bucket = 'lovelywater'

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
    url = f'https://s3.amazonaws.com/{bucket}/{file_key}'
    file_response = urllib.request.urlopen(url)
    return file_response.read().decode('utf-8')
