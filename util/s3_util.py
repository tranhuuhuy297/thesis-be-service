import boto3
from botocore.exceptions import ClientError

from util.logger_util import logger

AWS_S3_PREFIX = 'thh297-s3'


class S3:
    def __init__(self, region_name='ap-southeast-1', bucket_name='raw-data'):
        self.region_name = region_name
        self.bucket_name = self.norm_bucket_name(bucket_name)
        self.s3_client = boto3.client('s3', region_name=region_name)

        # create bucket if not exist
        if not self.check_exist_bucket():
            self.create_bucket()

    def norm_bucket_name(self, bucket_name):
        if bucket_name is None:
            return self.bucket_name
        return f'{AWS_S3_PREFIX}-{bucket_name}'

    def check_exist_bucket(self):
        s3 = boto3.resource('s3',
                            region_name=self.region_name)
        return s3.Bucket(self.bucket_name) in s3.buckets.all()

    def create_bucket(self):
        try:
            if self.region_name is None:
                return False
            else:
                location = {'LocationConstraint': self.region_name}
                self.s3_client.create_bucket(Bucket=self.bucket_name,
                                             CreateBucketConfiguration=location)
        except ClientError as e:
            logger.error(e)

    def put_object(self, object_data, object_name):
        try:
            self.s3_client.put_object(Body=object_data, Bucket=self.bucket_name, Key=str(object_name))
        except ClientError as e:
            logger.error(e)
