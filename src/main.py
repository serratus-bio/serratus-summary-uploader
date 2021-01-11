from SraRun import SraRun
from Summary import Summary
from io import StringIO
import os
import json
from pathlib import Path

root_dir = 'out'
family_dir = os.path.join(root_dir, 'family')
sequence_dir = os.path.join(root_dir, 'sequence')
Path(root_dir).mkdir(parents=True, exist_ok=True)
Path(family_dir).mkdir(parents=True, exist_ok=True)
Path(sequence_dir).mkdir(parents=True, exist_ok=True)

run_id = 'ERR2756789'
run = SraRun(run_id)
summary = run.get_summary()
summary = Summary(StringIO(summary))

out_dir = family_dir
for family in summary.families:
    out_fn = f'{run.name}_{family["fam"]}.json'
    out_fp = os.path.join(out_dir, out_fn)
    with open(out_fp, 'w') as f:
        json.dump(family, f)

out_dir = sequence_dir
for sequence in summary.sequences:
    out_fn = f'{run.name}_{sequence["seq"]}.json'
    out_fp = os.path.join(out_dir, out_fn)
    with open(out_fp, 'w') as f:
        json.dump(sequence, f)
