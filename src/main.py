from Summary import Summary
from summary_download import get_run_ids

for run_id in get_run_ids():
    print(run_id)
    summary = Summary(run_id)
    summary.upload()
