import boto3
import json
import csv


# Create SQS client
sqs = boto3.client('sqs')
queue_url = """[REPLACE THIS BY SQS QUEUE URL]"""


# Receive the message from SQS queue
def receive_msg(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    message = response['Messages'][0]
    return message


# Delete the received message from queue
def delete_msg(receipt_handle, queue_url):
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)



message = receive_msg(queue_url)    # Store the received message to message var

receipt_handle = message['ReceiptHandle']   # Store the receipt handle of the message to pass it to delete_msg method
delete_msg(receipt_handle, queue_url)   # Delete the message to avoid use it more than one time


# Extract the S3 bucket's name and key from the message
message_body = message['Body']
json_file = json.loads(message_body)
message_json = json.loads(json_file["Message"])
s3_bucket_key = message_json["Records"][0]["s3"]["object"]["key"]    
s3_bucket = message_json["Records"][0]["s3"]["bucket"]["name"]  


# Exporting a list variable into the csv file
input_variable = [s3_bucket, s3_bucket_key]


# db.csv gets created in the current working directory
with open('db.csv', 'w', newline = '') as csvfile:
	my_writer = csv.writer(csvfile, delimiter = ':')
	my_writer.writerow(input_variable)





