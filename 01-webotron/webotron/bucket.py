# -*- coding: utf-8 -*-

# Classes for S3 Bucket Managment

import boto3
from botocore.exceptions import ClientError

class BucketManager:
    """Manage an S3 Bucket."""

    def __init__(self, session):
        """Create a BucketManager object."""
        self.session = session
        self.s3 = self.session.resource("s3")

    def all_buckets(self):
        """Returns all buckets from AWS Account"""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Returns all objects from a bucket"""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create new bucket or return existing."""
        s3_bucket = None

        try:
            s3_bucket = self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self.session.region_name}
        )
        except ClientError as e:
            if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise e

        return s3_bucket

    def set_policy(self, bucket):
        """Set bucket policy for public websites."""
        policy = """
        {
        "Version": "2012-10-17",
        "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
                "Action":["s3:GetObject"],
                "Resource":["arn:aws:s3:::%s/*"]
                }
            ]
        }
        """ % bucket.name
        policy = policy.strip()

        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        """Configure S3 Website hosting settings."""
        bucket.Website().put(WebsiteConfiguration={
            "ErrorDocument": {
                "Key": "error.html"
            },
            "IndexDocument": {
                "Suffix": "index.html"
            }
        })