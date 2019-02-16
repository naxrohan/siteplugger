import boto3
import os
import time
from dateutil import tz
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


class dynamoplugger:
    'Dynamodb SitePlugger class'

    dynamodb = ""
    table = ""
    tablename = "URLCollection"

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

    def list_tables(self):
        response = {}
        try:
            self.dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
            response = self.dynamodb.list_tables(
                ExclusiveStartTableName='URL',
                Limit=100
            )
        except ClientError as ex:
            print ex.response['Error']

        return response['TableNames']

    def create_table(self):

        try:
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
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
        except ClientError as ex:
            print ex.response['Error']

        # Wait until the table exists.
        # self.table.meta.client.get_waiter('table_exists').wait(TableName=self.tablename)
        # print self.table

        # Print out some data about the table.
        return self.table

    def insert_item(self, urls, content, status):
        print " {} --> {} -->{} \n".format(urls, content, status)
        response = {}
        try:
            self.table = self.dynamodb.Table(self.tablename)
            response = self.table.put_item(
                Item={
                    'URLTitle': urls,
                    'URLContent': content,
                    'URLStatus': status,
                }
            )
        except ClientError as ex:
            print ex.response['Error']

        return response

    def get_all_row(self, limit, status):
        response = {}
        try:
            self.table = self.dynamodb.Table(self.tablename)
            response = self.table.scan(
                FilterExpression=Key('URLStatus').eq(status),
                ProjectionExpression="#US, URLTitle",
                ExpressionAttributeNames={'#US': 'URLStatus'},
                Limit=limit,
            )
        except ClientError as ex:
            print ex.response['Error']

        item = response['Items']
        return item

    def get_one_item(self, title_key, status):
        response = {}
        try:
            self.dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

            response = self.dynamodb.get_item(
                Key={
                    'URLTitle': {
                        'S': title_key
                    },
                    'URLStatus': {
                        'N': status
                    },
                },
                TableName=self.tablename,
            )
        except ClientError as ex:
            print ex.response['Error']

        if 'Item' in response:
            return response['Item']
        else:
            return response

    def update_one_row(self, url, content_set):
        response = {}
        try:
            self.table = self.dynamodb.Table(self.tablename)
            response = self.table.update_item(
                Key={
                    'URLStatus': 1,
                    'URLTitle': url
                },
                UpdateExpression='SET URLContent = :val1',
                ExpressionAttributeValues={
                    ':val1': content_set
                }
            )
        except ClientError as ex:
            print ex.response['Error']

        return response

    def import_all_links_to_db(self):
        # Insert all links from file to table:
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
                try:
                    print self.insert_item(final_url, "abc", 1)
                except ClientError as ex:
                    print ex.response['Error']


# dynamo = dynamoplugger
# url_string = 'https://disciplesofhope.wordpress.com/tag/avoiding-deception'
# print dynamo.create_table(dynamoplugger())
# print dynamo.list_tables(dynamoplugger())
# print dynamo.get_all_row(dynamoplugger(), 1000, 1)
# print dynamo.get_one_item(dynamoplugger(), url_string, '1')
# print dynamo.update_one_row(dynamoplugger(), url_string, "adasdascmasconsosfd")

# dynamo.import_all_links_to_db(dynamoplugger())

