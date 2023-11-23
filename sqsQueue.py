import boto3

# Get the service resource
# sqs = boto3.client('sqs', region_name='us-east-1')

# Create the queue. 
sqs_client = boto3.client(
  "sqs", 
  region_name="us-east-1", 
  aws_access_key_id='AKIA3XW3AFUMDMXLXCU4',
  aws_secret_access_key='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')

response = sqs_client.create_queue(
    QueueName="test_gcp",
    Attributes={
        "DelaySeconds": "0",
        "VisibilityTimeout": "60",  # 60 seconds
    }
)
print(response) #Printing queue url