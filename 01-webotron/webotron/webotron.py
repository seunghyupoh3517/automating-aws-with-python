#!/usr/bin/python  :#! interpreter for each language tot ell what interpreter should run it
# -*- coding: utf-8 -*-

"""webotron: Deploy websites with aws.

Webotron automates the process of deploying static websites to AWSselfself.
- Configure AWS s3 list_bucket
    - Create them
    - Set them up for static website hosting
    - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS

## it's a good habit to leave the comments in the doc string.
"""
import boto3
import sys
import click

from bucket import BucketManager

session = boto3.Session(profile_name='PythonAutomation')
bucket_manager = BucketManager(session) ## bucket manager will later hold S3 resource
#S3 = session.resource('s3')


@click.group()
def cli():
    """Webtron delpoys websites to AWS."""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.s3.buckets.all():
        print (bucket)
## Document string use --help
@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an s3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and Configure s3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    # s3_bucket = bucket_manager.s3.Bucket(bucket)
    bucket_manager.sync(pathname, bucket)

# a single file in python is treated as module But
# if you want to run it as a script give __name__ == '__main__'
if __name__ == '__main__':
    #list_buckets()
    cli()
## python convention
## when this file run as script _name_ will be equalized _main_
