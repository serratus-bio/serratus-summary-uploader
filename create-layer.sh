pip install -r requirements.txt 
mkdir -p tmp/python
cp -rp ve/lib/python3.8/site-packages/* tmp/python
pushd tmp
zip -r9 -q ../layer.zip python
popd
rm -r tmp
