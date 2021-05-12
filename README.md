# Use Boto3 on AWS for Message Queuing
A Boto3 (AWS SDK for Python) script to automate pull messages from SQS queue and download files from S3 bucket by push notification to SNS and the SNS send the message to the subscripes (Email and Two SQS queues)

So, in this repository we will:
- **First**:
  - Create SNS topic and add access policy to allow S3 to push notifications to SNS topic on events.
  - Configure event notification on S3 with the SNS topic.
  - Add your E-mail to SNS subscripers to receive an email once event happened on the S3.
  - Create 3 SQS queues:
     - The first and the second SQS queues will be subscriped in the SNS topic to receive messages once S3 event happened.
     - Add access policy to the first and the second SQS queues for S3.
     - The Third SQS queue will be the Dead Letter queue of the first SQS queue.
     
- **Second**: 
  - Make a Boto3 python script called (validator.py) to: 
    - pull the messages from the first SQS queue.
    - Extract the key name of the file in the S3 bucket.
    - Download this file and make some changes on it.
    - Upload the modified file to another S3 bucket.
  
  - Make another Boto3 python script called (metadata.py) to:
    - pull the messages from the second SQS queue.
    - Extract the metadata of the S3 bucket (S3 bucket name & The file name).
    - And save the metadata in a CSV file called (db.csv).
