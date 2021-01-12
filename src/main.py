from Summary import Summary
from summary_download import get_run_ids
from summary_upload import upload_summary

for run_id in get_run_ids():
    summary = Summary(run_id)
    print(summary)
    upload_summary(summary)
