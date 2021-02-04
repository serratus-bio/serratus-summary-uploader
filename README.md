# serratus-summary-uploader

Uploads files to Aurora Serverless.

For previous iteration using Athena, see [athena.md](doc/athena.md).

## Overview

For each SRA run processed by Serratus:

1. Download summary files from `s3://lovelywater/summary2/`
2. Parse and upload files into 1 table per summary section.

## Lambda events

### Manager

Seed event:

```json
{
  "type": "protein"
}
```

### Worker

Process 5 SRA runs:

```json
{
  "type": "protein",
  "start_byte": 0,
  "end_byte": 49
}
```

Clear tables:

```json
{
  "type": "protein",
  "clear": true
}
```

## AWS Setup

### Aurora Serverless

- standard create
- engine type
    - engine type: aurora
    - edition: postgresql compatibility
    - capacity type: serverless
    - version: aurora postgresql (comatible w/ postgresql 10.12)
- settings
    - db cluster id: serratus-aurora
    - master username: serratus
    - pw: auto-gen
- capacity settings
    - default min/max
    - pause after 5m
- connectivity
    - vpc: serratus-aurora-vpc
    - create new db subnet group
    - vpc sg: serratus-aurora-sg
    - web service data api: enable
- additional
    - initial db: `summary`
    - backup retention: 1d
    - disable copy tags
    - enable deletion protection

### Lambda

2 Lambda functions:

- `serratus-summary-uploader-manager`
- `serratus-summary-uploader-worker`

`manager` iterates over `s3://serratus-athena/index.txt` and calls `worker` per batch of lines.

#### Manager lambda

- Role: `serratus-summary-uploader-manager-role`
- Environment variables
    ```json
    {
        "WORKER_LAMBDA": "serratus-summary-uploader-worker",
        "INDEX_BUCKET": "serratus-summary-uploader",
        "NUCLEOTIDE_INDEX": "nindex.txt",
        "PROTEIN_INDEX": "pindex.txt",
        "RDRP_INDEX": "rindex.txt"
    }
    ```
- Handler: `main.handler`
- Timeout: 1m
- Concurrency: 10
- Retry attempts: 0

#### Worker lambda

- Role: `serratus-summary-uploader-worker-role`
- Environment variables
    ```json
    {
        "INDEX_BUCKET": "serratus-summary-uploader",
        "NUCLEOTIDE_INDEX": "nindex.txt",
        "PROTEIN_INDEX": "pindex.txt",
        "RDRP_INDEX": "rindex.txt"
    }
    ```
- Handler: `main.handler`
- Timeout: 15m
- Memory: 10240MB (max)
- Concurrency: unreserved
- Layer:
    - https://aws-data-wrangler.readthedocs.io/en/stable/install.html#aws-lambda-layer

### S3

- bucket name: `serratus-summary-uploader`
- policy

    ```json
    {
        "Sid": "serratus-summary-uploader-manager",
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::797308887321:role/service-role/serratus-summary-uploader-manager-role"
        },
        "Action": [
            "s3:GetObject"
        ],
        "Resource": [
            "arn:aws:s3:::serratus-summary-uploader/*"
        ]
    },
    {
        "Sid": "serratus-summary-uploader-worker",
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::797308887321:role/service-role/serratus-summary-uploader-worker-role"
        },
        "Action": [
            "s3:GetObject"
        ],
        "Resource": [
            "arn:aws:s3:::serratus-summary-uploader/*"
        ]
    }
    ```

### IAM

Inline policy for `serratus-summary-uploader-manager-role`:

Name: `InvokeFunctionInAccount`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": "*"
        }
    ]
}
```

Inline policy for `serratus-summary-uploader-worker-role`:

Name: `RDSDataApi`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rds-data:*"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

- add `s3:*` for `clear()`

## Miscellaneous

### TODO

- separate events for `upload_init` vs. `upload`

### Handy commands

```sh
# generate index
sed 's/...............................//g' pindex.tsv | sed 's/.psummary//g' > pindex.txt
```

### Lambda Throttling

- Select **Throttle** in UI and confirm
- Asynchronous invocation:
    - Maximum age of event: `0h 1m 0s`
    - Retry attempts: `0`
