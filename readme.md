Runner.py ---help article 
 
 Options below: 
 
 `scan_pages  - to scan for new pages in site.`
 
 `local_saver - to save new pages that are found.`
 
 `write_s3    - copy new files to s3 bucket.`

Run local Dynamo db instance 
 
 `docker run -p 8000:8000 amazon/dynamodb-local`
 `http://localhost:8000/shell/`
 
 
 Deploy code to lambda:
 
 `aws lambda update-function-code --function-name siteplugger --zip-file fileb://function.zip`
 
 