# coding: utf-8

import boto3
from pathlib import Path

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource("s3")
s3_client = session.client('s3')

bucket = s3.create_bucket(Bucket='xxx',CreateBucketConfiguration={"LocationConstraint": session.region_name})

pathname = 'C:/Users/xxx/Downloads/Pexels Videos 2795164.mp4
path = Path(pathname).expanduser().resolve()

s3_client.upload_file(
            Filename = str(path),
            Bucket = 'kilpavidtest',
            Key = path.name)

rekognition_client = session.client('rekognition')                
               
response = rekognition_client.start_label_detection(Video={'S3Object': { 'Bucket': 'kilpavidtest', 'Name': 'Pexels Videos 2795164.mp4'}})                    

job_id = response['JobId']

print(job_id)

result = rekognition_client.get_label_detection(JobId=job_id)

result['Labels']

len(result['Labels'])
