# -*- coding: utf-8 -*-

# Classes for S3 Bucket Managment

class BucketManager:
    """Manage an S3 Bucket."""

    def __init__(self, session):
        """Create a BucketManager object."""
        self.s3 = session.resource("s3")

    def all_buckets(self):
        """Returns all buckets from AWS Account"""
        return self.s3.buckets.all()

    def all_objects(self, bucket):
        """Returns all objects from a bucket"""
        return self.s3.Bucket(bucket).objects.all()

