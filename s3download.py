import boto3

# Replace 'your_access_key_id' and 'your_secret_access_key' with your AWS credentials
access_key_id = '<your_access_key_id>'
secret_access_key = '<your_secret_access_key>'

# Replace 'your_bucket_name' with the name of your S3 bucket
bucket_name = '<your_bucket_name>'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

# Path of the file in S3
object_key = 'file/location/someFile.txt'

# save the file in the current directory.
local_file_path = "./someFile.txt"

# Download the object from S3
s3.download_file(bucket_name, object_key, local_file_path)

print(f"Object '{object_key}' downloaded to '{local_file_path}'")