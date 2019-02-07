Runner.py ---help article 
 
 Options below: 
 
 `scan_pages  - to scan for new pages in site.`
 
 `local_saver - to save new pages that are found.`
 
 `write_s3    - copy new files to s3 bucket.`
 
 
 `docker run -p 8000:8000 amazon/dynamodb-local`
 
 `aws lambda update-function-code --function-name siteplugger --zip-file fileb://function.zip`
 
 
 aws dynamodb create-table 
    --table-name URLCollection 
    --attribute-definitions 
        AttributeName=URL,AttributeType=S 	
        AttributeName=Status,AttributeType=S 
        AttributeName=URLContent,AttributeType=S 
    --key-schema 
        AttributeName=URL,KeyType=HASH 
        AttributeName=URLContent,KeyType=HASH 	
        AttributeName=Status,KeyType=RANGE 
    --provisioned-throughput 
        ReadCapacityUnits=5,WriteCapacityUnits=5 
    --endpoint-url 
        http://localhost:8000