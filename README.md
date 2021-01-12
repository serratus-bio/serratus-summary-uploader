# serratus-summary-uploader

Uploads files to `s3://serratus-athena` to be queried via [serratus-summary-api](https://github.com/serratus-bio/serratus-summary-api).

## Usage

```
python main.py
```

For each SRA run processed by Serratus:

1. Download summary file from `s3://lovelywater/summary2/`
2. Parse file into JSON format
3. Upload files to `s3://serratus-athena/run/`, `s3://serratus-athena/family/`, and `s3://serratus-athena/sequence/`

## TODO

- parallelized download (via `NextContinuationToken`)
- check if a run is already processed (presence of `serratus-athena/run/<run_id>.json`)
