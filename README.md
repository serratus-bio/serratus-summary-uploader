# serratus-summary-uploader

Uploads files to `s3://serratus-athena` to be queried via [serratus-summary-api](https://github.com/serratus-bio/serratus-summary-api).

## Overview

For each SRA run processed by Serratus:

1. Download summary file from `s3://lovelywater/summary2/`
2. Parse file into JSON format
3. Upload files:
    - `s3://serratus-athena/run/<RUN>.json`
    - `s3://serratus-athena/family/<RUN>_<FAMILY>.json`
    - `s3://serratus-athena/sequence/<RUN>_<SEQUENCE>.json`

## AWS Setup

### Lambda

2 Lambda functions:

- `serratus-summary-uploader-batch`
- `serratus-summary-uploader-single`

`batch` iterates over `s3://serratus-athena/index.txt` and calls `single` per line (`run_id`).

#### Batch lambda

- Role: `serratus-summary-uploader-batch-role`
- Environment variables
    ```json
    {
        "WORKER_LAMBDA": "serratus-summary-uploader-single",
        "INDEX_BUCKET": "serratus-athena",
        "INDEX_FILE": "index.txt"
    }
    ```
- Timeout: 15m
- Concurrency: unreserved
- Retry attempts: 0

#### Worker lambda

- Role: `serratus-summary-uploader-single-role`
- Environment variables
    ```json
    {
        "INDEX_BUCKET": "serratus-athena",
        "INDEX_FILE": "index.txt"
    }
    ```
- Timeout: 15m
- Memory: 10240MB (max)
- Concurrency: unreserved
- Layer:
    - https://aws-data-wrangler.readthedocs.io/en/stable/install.html#aws-lambda-layer

### S3

#### Download bucket policy

```json
{
    "Sid": "serratus-summary-uploader-single",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::797308887321:role/service-role/serratus-summary-uploader-single-role"
    },
    "Action": [
        "s3:ListBucket",
        "s3:GetObject"
    ],
    "Resource": [
        "arn:aws:s3:::lovelywater",
        "arn:aws:s3:::lovelywater/*"
    ]
}
```

#### Upload bucket policy

```json
{
    "Sid": "serratus-summary-uploader-single",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::797308887321:role/service-role/serratus-summary-uploader-single-role"
    },
    "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:PutObjectAcl"
    ],
    "Resource": [
        "arn:aws:s3:::serratus-athena",
        "arn:aws:s3:::serratus-athena/*"
    ]
},
{
    "Sid": "serratus-summary-uploader-batch",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::797308887321:role/service-role/serratus-summary-uploader-batch-role"
    },
    "Action": [
        "s3:GetObject"
    ],
    "Resource": [
        "arn:aws:s3:::serratus-athena/*"
    ]
}
```

### IAM

Inline policy for `serratus-summary-uploader-batch-role`:

Name: `InvokeFunctionInAccount`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": "arn:aws:lambda:*:797308887321:function:*"
        }
    ]
}
```

Inline policy for `serratus-summary-uploader-single-role`:

Name: `Glue`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "glue:BatchCreatePartition",
                "glue:GetDatabase",
                "glue:GetPartition",
                "glue:CreateTable",
                "glue:CreateSchema",
                "glue:DeleteTable",
                "glue:CreatePartition",
                "glue:GetSchema",
                "glue:GetTable"
            ],
            "Resource": "*"
        }
    ]
}
```

- add `s3:*` for `clear()`

## Miscellaneous

### TODO

- rename `single` to `worker`
- `psummary` files

### Sources of inspiration

- https://medium.com/swlh/processing-large-s3-files-with-aws-lambda-2c5840ae5c91
- https://medium.com/analytics-vidhya/demystifying-aws-lambda-deal-with-large-files-stored-on-s3-using-python-and-boto3-6078d0e2b9df
- https://www.reddit.com/r/aws/comments/b73lis/processing_a_large_csv_file_with_a_lambda_line_by/
- bandwidth: https://www.reddit.com/r/aws/comments/ev9u8f/aws_lambda_maximum_bandwidth_05_gbps/

### Handy commands

```sh
# force reprocessing
aws s3 rm s3://serratus-athena/run/ --recursive

# sync summary2
aws s3 sync s3://lovelywater/summary2/ s3://serratus-athena/summary2/ --include "*" --quiet
```

### Lambda Throttling

- Select **Throttle** in UI and confirm
- Asynchronous invocation:
    - Maximum age of event: `0h 1m 0s`
    - Retry attempts: `0`
