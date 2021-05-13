# Use Boto3 on AWS for Message Queuing
A Boto3 (AWS SDK for Python) script to automate pull messages from SQS queue and download files from S3 bucket by push notification to SNS and the SNS send the message to the subscribes (Email and Two SQS queues)


## Prerequisites
- AWS account
- Boto3 

## First step:
  - Create SNS topic and add an access policy to allow S3 to push notifications to SNS topic on events.
  - Configure event notification on S3 with the SNS topic.
  - Add your E-mail to SNS subscribers to receive an email once the event happened on the S3.
  - Create 3 SQS queues:
     - The first and the second SQS queues will be subscribed to the SNS topic to receive messages once S3 event happened.
     - Add access policy to the first and the second SQS queues for S3.
     - The Third SQS queue will be the Dead Letter queue of the first SQS queue.

## Second step:
- Make a Boto3 python script called (validator.py) to: 
    - pull the messages from the first SQS queue.
    - Extract the key name of the file in the S3 bucket.
    - Download this file and make some changes on it.
    - Upload the modified file to another S3 bucket.
  
  - Make another Boto3 python script called (metadata.py) to:
    - pull the messages from the second SQS queue.
    - Extract the metadata of the S3 bucket (S3 bucket name & The file name).
    - And save the metadata in a CSV file called (db.csv).

## The Architecture
![terminal screenshot](https://raw.githubusercontent.com/Ahmedsamymahrous/Boto3-AWS-MessageQueuing/main/image_for_illustration.jpg)
