import time
import urllib

nucleotide_dir = 'summary2'
nucleotide_suffix = '.summary'
protein_dir = 'psummary'
protein_suffix = '.psummary'
rdrp_dir = 'rsummary'
rdrp_suffix = '.psummary'

def get_nucleotide(run_id):
    file_key = f'{nucleotide_dir}/{run_id}{nucleotide_suffix}'
    return get_file_contents('lovelywater', file_key)

def get_protein(run_id):
    file_key = f'{protein_dir}/{run_id}{protein_suffix}'
    return get_file_contents('lovelywater', file_key)

def get_rdrp(run_id):
    file_key = f'{rdrp_dir}/{run_id}{rdrp_suffix}'
    return get_file_contents('serratus-bio', file_key)

def get_file_contents(bucket, file_key):
    url = f'https://s3.amazonaws.com/{bucket}/{file_key}'
    retry_count = 0
    while retry_count < 5:
        try:
            return get_url_contents(url)
        except (ConnectionResetError, urllib.error.URLError):
            retry_count += 1
            time.sleep(2 ** retry_count)
    return get_url_contents(url)

def get_url_contents(url):
    file_response = urllib.request.urlopen(url)
    return file_response.read().decode('utf-8')
