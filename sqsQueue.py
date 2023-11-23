import boto3

# Get the service resource
# sqs = boto3.client('sqs', region_name='us-east-1')

# Create the queue. 
sqs_client = boto3.client(
  "sqs", 
  region_name="us-east-1")

response = sqs_client.create_queue(
    QueueName="test_new_credential",
    Attributes={
        "DelaySeconds": "0",
        "VisibilityTimeout": "60",  # 60 seconds
    }
)
print(response) #Printing queue url