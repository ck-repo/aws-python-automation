#!/usr/bin/python
# -*- coding: utf-8 -*-

# Webotron automates the deployment of static websites to S3

import mimetypes
import boto3
import click
from bucket import BucketManager

session = None
bucket_manager = None
s3_client = None

@click.group()
@click.option("--profile", default=None,
    help="Choose an AWS profile to use while executing commands")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager, s3_client

    session_cfg = {}
    if profile:
        session_cfg["profile_name"] = profile

    session = boto3.Session(**session_cfg)
    s3_client = session.client('s3')
    bucket_manager = BucketManager(session)
    pass


@cli.command("list-buckets")
def list_buckets():
    """List all S3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command("list-bucket-objects")
@click.argument("bucket")
def list_bucket_objects(bucket):
    """List objects inside an S3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command("setup-bucket")
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure an S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)

    bucket_manager.set_policy(s3_bucket)

    bucket_manager.configure_website(s3_bucket)

    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))

    return

@cli.command("upload-file")
@click.argument("file_name")
@click.argument("bucket")
@click.argument("key")
def upload_file(file_name, bucket, key):
    """Upload File to S3 Bucket."""

    content_type = mimetypes.guess_type(key)[0]

    try:
        response = s3_client.upload_file(
            file_name,
            bucket,
            key,
            ExtraArgs={
                "ContentType": "text/html"
            })
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == '__main__':
    cli()
