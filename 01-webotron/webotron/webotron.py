#!/usr/bin/python
# -*- coding: utf-8 -*-

# Webotron automates the deployment of static websites to S3

import mimetypes
import boto3
import click
from webotron.bucket import BucketManager
from webotron.domain import DomainManager
from webotron import util
from webotron.certificate import CertificateManager
from webotron.cdn import DistributionManager

session = None
bucket_manager = None
s3_client = None
cert_manager = None
dist_manager = None


@click.group()
@click.option("--profile", default=None,
    help="Choose an AWS profile to use while executing commands")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager, s3_client, domain_manager, cert_manager, dist_manager

    session_cfg = {}
    if profile:
        session_cfg["profile_name"] = profile

    session = boto3.Session(**session_cfg)
    s3_client = session.client('s3')
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)
    cert_manager = CertificateManager(session)
    dist_manager = DistributionManager(session)

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



@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure R53 Domain to point to S3 Bucket."""
    bucket = bucket_manager.get_bucket(domain)

    zone = domain_manager.find_hosted_zone(domain) \
        or domain_manager.create_hosted_zone(domain)

    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))
    domain_manager.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configure: http://{}".format(domain))

#bucket name must be same as website url/DNS name for setup-domain to work

@cli.command("find-cert")
@click.argument("domain")
def find_cert(domain):
    """Lists Certificates from ACM."""
    print(cert_manager.find_matching_cert(domain))

@cli.command('setup-cdn')
@click.argument('domain')
@click.argument('bucket')
def setup_cdn(domain, bucket):
    """Set up CloudFront CDN for Domain pointing to S3 Bucket."""
    dist = dist_manager.find_matching_dist(domain)

    if not dist:
        cert = cert_manager.find_matching_cert(domain)
        if not cert:  # SSL is not optional at this time
            print("Error: No matching cert found.")
            return

        dist = dist_manager.create_dist(domain, cert)
        print("Waiting for distribution deployment...")
        dist_manager.await_deploy(dist)

    zone = domain_manager.find_hosted_zone(domain) \
        or domain_manager.create_hosted_zone(domain)

    domain_manager.create_cf_domain_record(zone, domain, dist['DomainName'])
    print("Domain configured: https://{}".format(domain))

    return

if __name__ == '__main__':
    cli()
