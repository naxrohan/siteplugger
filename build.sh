#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
  echo "Usage : ./build.sh lambdaName";
  exit 1;
fi

echo $1

echo "removing old zip"
rm archive.zip;

echo "creating a new zip file"
zip archive.zip *  -r -x .git/\* \*.sh \*.md \*.gitignore tests/\* venv/\* site-plugger/\* .idea/\* node_modules/aws-sdk/\* \*.zip

echo "Uploading $1 to us-east-1";

aws lambda update-function-code --function-name $1 --zip-file fileb://archive.zip --publish

if [ $? -eq 0 ]; then
  echo "!! Upload successful !! -->$2"

#  aws lambda invoke --function-name $1 --log-type Tail --payload '{"cmd":"$2"}' output.txt

#  cat output.txt

else 
  echo "Upload failed"
  echo "If the error was a 400, check that there are no slashes in your lambda name"
  echo "Lambda name = $1"
  exit 1;
fi

