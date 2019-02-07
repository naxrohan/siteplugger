import boto3
import os
import time

class dynamoplugger:
    'Dynamodb SitePlugger class'

    dynamodb = ""
    table = ""
    tablename = "URLCollection"

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def create_table(self):

        # Create the DynamoDB table.
        self.table = self.dynamodb.create_table(
            TableName=self.tablename,
            KeySchema=[
                {
                    'AttributeName': 'URLTitle',
                    'KeyType': 'HASH'
                },
                # {
                #     'AttributeName': 'URLContent',
                #     'KeyType': 'HASH'
                # },
                {
                    'AttributeName': 'URLStatus',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'URLTitle',
                    'AttributeType': 'S'
                },
                # {
                #     'AttributeName': 'URLContent',
                #     'AttributeType': 'S'
                # },
                {
                    'AttributeName': 'URLStatus',
                    'AttributeType': 'N'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        self.table.meta.client.get_waiter('table_exists').wait(TableName=self.tablename)

        # Print out some data about the table.
        return self.table.item_count

    def insert_item(self, urls, content, status):
        print " {} --> {} -->{} \n".format(urls, content, status)
        self.table = self.dynamodb.Table(self.tablename)
        response = self.table.put_item(
            Item={
                'URLTitle': urls,
                'URLContent': content,
                'URLStatus': status,
            }
        )
        return response

    def get_one_row(self, urls):
        self.table = self.dynamodb.Table(self.tablename)
        response = self.table.get_item(
            Key={
                'URLTitle': urls
            }
        )
        item = response['Item']
        return item

    def get_all_item(self):
        self.table = self.dynamodb.Table(self.tablename)
        response = self.table.get_item(
            Key={
                'URLTitle': '*'
            }
        )
        item = response['Item']
        return item

    def update_one_row(self, url):
        self.table = self.dynamodb.Table(self.tablename)
        response = self.table.update_item(
            Key={
                'URLStatus': "1",
            },
            UpdateExpression='SET URLStatus = :val1',
            ExpressionAttributeValues={
                ':val1': url
            }
        )
        return response


dynamo = dynamoplugger

# print dynamo.create_table(dynamoplugger())

final_log_path = "site-plugger/scanner_log_.txt"
readfp = open(final_log_path, "r")
log_file_size = os.path.getsize(final_log_path)
log_content = readfp.read(log_file_size)
if log_content != False:
    readfp.close()
    allreadline = log_content.split("\n")
    final_array = []

    if allreadline is not []:
        final_array = list(set(allreadline))
    else:
        print "no file log exist?"

for final_url in final_array:
    if final_url.strip(" ") != "":
        time.sleep(1)
        print dynamo.insert_item(dynamoplugger(), final_url, "abc", 1)


