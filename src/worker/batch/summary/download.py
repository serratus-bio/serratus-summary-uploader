import time
import urllib


def get_summary_file(run_id, bucket, prefix, suffix):
    """Return contents of a Serratus summary file.

    The summary file format is described in:
    https://github.com/ababaian/serratus/wiki/.summary-Reports
    """
    url = f'https://s3.amazonaws.com/{bucket}/{prefix}{run_id}{suffix}'
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
