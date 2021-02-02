cd src

pushd worker
zip -rq package .
aws lambda update-function-code \
    --function-name serratus-summary-uploader-worker \
    --zip-file fileb://./package.zip
rm package.zip
popd

pushd manager
zip -rq package .
aws lambda update-function-code \
    --function-name serratus-summary-uploader-manager \
    --zip-file fileb://./package.zip
rm package.zip
popd
