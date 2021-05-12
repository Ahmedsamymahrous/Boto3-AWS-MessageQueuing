import boto3
import json
import botocore


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


# Download the file from the first S3 bucket
def download_file(bucket_download, s3_bucket_key):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket_download).download_file(s3_bucket_key, s3_bucket_key)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


# Upload the modified file to the second S3 bucket
def upload_file(new_file_name, bucket_upload, object_name=None):

    if object_name is None:
        object_name = new_file_name

    s3_client = boto3.client('s3')
    response = s3_client.upload_file(new_file_name, bucket_upload, object_name)
    
    return True


# Make some changes in the file to upload it to the second S3 bucket 
def change_the_file(s3_bucket_key):
    f1 = open(s3_bucket_key, "r")
    output = f1.read()
    new_input = output.replace(',', '\n')

    f2 = open(s3_bucket_key,"w")
    f2.write(new_input)
    f1.close()
    f2.close()




message = receive_msg(queue_url)    # Store the received message to message var

receipt_handle = message['ReceiptHandle']   # Store the receipt handle of the message to pass it to delete_msg method
delete_msg(receipt_handle, queue_url)   # Delete the message to avoid use it more than one time


# Extract the S3 bucket's key from the message
message_body = message['Body']
json_file = json.loads(message_body)
message_json = json.loads(json_file["Message"])
s3_bucket_key = message_json["Records"][0]["s3"]["object"]["key"]


bucket_download = """[REPLACE THIS BY THE S3 BUCKET NAME]""" # The bucket that we will download from
bucket_upload = """[REPLACE THIS BY THE S3 BUCKET NAME]"""   # The bucket that we will upload to

download_file(bucket_download, s3_bucket_key)   # 1: download file from the first S3
change_the_file(s3_bucket_key)                  # 2: change the file content
upload_file(s3_bucket_key, bucket_upload)       # 3: upload the file to the second S3 bucket 



