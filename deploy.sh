cd src

pushd lambda_worker
zip -rq package .
aws lambda update-function-code \
    --function-name serratus-summary-uploader-single \
    --zip-file fileb://./package.zip
rm package.zip
popd

pushd lambda_batch
zip -rq package .
aws lambda update-function-code \
    --function-name serratus-summary-uploader-batch \
    --zip-file fileb://./package.zip
rm package.zip
popd
