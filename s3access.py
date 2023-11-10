import boto3

# Replace 'your_access_key_id' and 'your_secret_access_key' with your AWS credentials
access_key_id = '<your_access_key_id>'
secret_access_key = '<your_secret_access_key>'

# Replace 'your_bucket_name' with the name of your S3 bucket
bucket_name = '<your_bucket_name>'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

# List all objects in the bucket
response = s3.list_objects(Bucket=bucket_name)

# Print the object details
print("Objects in the bucket:")
for obj in response.get('Contents', []):
    print(f"- {obj['Key']} (Last modified: {obj['LastModified']})")