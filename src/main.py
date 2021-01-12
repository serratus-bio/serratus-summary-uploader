from Summary import Summary
from summary_download import get_run_ids
import os
import json
from pathlib import Path

root_dir = 'out'
family_dir = os.path.join(root_dir, 'family')
sequence_dir = os.path.join(root_dir, 'sequence')
Path(root_dir).mkdir(parents=True, exist_ok=True)
Path(family_dir).mkdir(parents=True, exist_ok=True)
Path(sequence_dir).mkdir(parents=True, exist_ok=True)

for run_id in get_run_ids():
    summary = Summary(run_id)
    print(summary)
    out_dir = family_dir
    for family in summary.families:
        out_fn = f'{summary.run_id}_{family["fam"]}.json'
        out_fp = os.path.join(out_dir, out_fn)
        with open(out_fp, 'w') as f:
            json.dump(family, f)

    out_dir = sequence_dir
    for sequence in summary.sequences:
        out_fn = f'{summary.run_id}_{sequence["seq"]}.json'
        out_fp = os.path.join(out_dir, out_fn)
        with open(out_fp, 'w') as f:
            json.dump(sequence, f)

    # TODO: summary.properties
