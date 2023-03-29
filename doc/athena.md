# serratus-summary-uploader

Uploads files to `s3://serratus-athena` to be queried via [serratus-summary-api](https://github.com/serratus-bio/serratus-summary-api).

## Overview

For each batch of SRA runs processed by Serratus:

1. Download summary files from `s3://lovelywater2/summary2/`
2. Load summary data into dataframes (1 per summary section)
3. Upload dataframes as parquet:
   - `s3://serratus-athena/protein/score=x/pctid=y/z.parquet`
   - `s3://serratus-athena/nucleotide/score=x/pctid=y/z.parquet`

## AWS Setup

### S3

#### Download bucket policy

Not needed - using direct HTTP calls on public bucket.

#### Index bucket policy

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
        "arn:aws:s3:::serratus-athena/*"
    ]
},
{
    "Sid": "serratus-summary-uploader-worker",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::797308887321:role/service-role/serratus-summary-uploader-manager-role"
    },
    "Action": [
        "s3:GetObject"
    ],
    "Resource": [
        "arn:aws:s3:::serratus-athena/*"
    ]
}
```

#### Upload bucket policy

```json
{
  "Sid": "serratus-summary-uploader-worker",
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::797308887321:role/service-role/serratus-summary-uploader-worker-role"
  },
  "Action": ["s3:PutObject", "s3:PutObjectAcl"],
  "Resource": ["arn:aws:s3:::serratus-athena", "arn:aws:s3:::serratus-athena/*"]
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
      "Resource": "arn:aws:lambda:*:797308887321:function:*"
    }
  ]
}
```

Inline policy for `serratus-summary-uploader-worker-role`:

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

- bucketing for fast filtering by `sra`
  - can't easily bucket w/ `awswrangler`
  - alternatively, use something similar to `serratus-api` (serve summary files directly w/ caching)
    - this will be hard to cross-reference on `sra` though

### Sources of inspiration

- https://medium.com/swlh/processing-large-s3-files-with-aws-lambda-2c5840ae5c91
- https://medium.com/analytics-vidhya/demystifying-aws-lambda-deal-with-large-files-stored-on-s3-using-python-and-boto3-6078d0e2b9df
- https://www.reddit.com/r/aws/comments/b73lis/processing_a_large_csv_file_with_a_lambda_line_by/
- bandwidth: https://www.reddit.com/r/aws/comments/ev9u8f/aws_lambda_maximum_bandwidth_05_gbps/
- merging multiple parquet files https://stackoverflow.com/questions/55461931/how-to-merge-multiple-parquet-files-in-glue
