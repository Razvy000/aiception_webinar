# https://aws.amazon.com/console/
# user > My Security Credentials > Continue to Security Credentials > Users > Add User
# username: raspi, access type: programmatic, permisisions: create group: raspigroup AmazonS3FullAccess > review create
# copy Access key ID
# copy Secret access key

# mkdir ~/.aws

# nano ~/.aws/credentials
# [default]
# aws_access_key_id = xxx
# aws_secret_access_key = xxx

# nano ~/.aws/config
# [default]
# region=eu-central-1

# create a bucket named 'raspi-bucket'
# services > s3 > create bucket > name, region > leave all default


# pip install boto3

# fancy naming scheme

import datetime
import time
import boto3

# create a client
client = boto3.client('s3')

# upload and set permission to public
bucket = 'raspi-bucket'
# bucket = 'blalblalbalb'

now = datetime.datetime.now()
key = '{}/{:02d}/image-{}.jpg'.format(now.year, now.month, int(time.time()))
# key = 'one_image.jpg'

client.upload_file('image.jpg', bucket, key, ExtraArgs={'ACL': 'public-read'})

# get the public url
file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket, key)
print(file_url)
